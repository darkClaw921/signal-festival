from fastapi import FastAPI, HTTPException,Form,Depends,Response, File, UploadFile
import requests
from pprint import pprint
import os
from dotenv import load_dotenv
# from fastapi.security import OAuth2PasswordBearer
load_dotenv()

from typing import Annotated
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from datetime import datetime
from pprint import pformat, pprint
from chat import GPT
from helper import prepare_table_for_text
from fastapi.responses import FileResponse
from pathlib import Path
from translation import transcript_audio
from fastapi.middleware.cors import CORSMiddleware
import aiohttp



gpt=GPT()
app = FastAPI(debug=False)
load_dotenv()
PORT = os.getenv('PORT_GENERATE_ANSWER')
HOST = os.getenv('HOST')
IP_SERVER = os.getenv('IP_SERVER')
HANDLER_MESSAGE_URL = os.getenv('HANDLER_MESSAGE_URL')

app = FastAPI(
    title="Signal System API",
    description="Generate answer API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Templates(directory="templates")
logs = []

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
MODELS_INDEX={
    'model_1': 'gpt2',
}
# Настройка CORS
origins = [
    "http://localhost:5173",  # Разрешите доступ с вашего фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все методы
    allow_headers=["*"],  # Разрешите все заголовки
)

# Убедитесь, что папка voice существует
os.makedirs("voice", exist_ok=True)

async def request_data(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,json=params) as response:
            return await response.text()

def update_or_create_model_index():
    global MODELS_INDEX
    # text=prepare_table_for_text()
    url='https://docs.google.com/document/d/1i77D_xI8x-Wsq11aIw-UBXgKMUbffeXwFSj1ckZogTI/edit?usp=sharing'
    text=gpt.load_prompt(url)
    MODELS_INDEX['main']=gpt.load_search_indexes(text)

    return MODELS_INDEX

update_or_create_model_index()
#  params = {'promt': promt, 'history': history, 'model_index': 'main', 'temp': 0.5, 'verbose': 1}
class Generate(BaseModel):
    #придет только то что тут есть если будут лишниые ключи то они не придут
    text: str
    model_index: str
    temp: float
    history: list
    promt: str
    verbose: int
    is_audio: bool

class Gen_Audio(BaseModel):
    text: str
    userID: int

@app.get("/generate-answer/")
# async def generate_answer(text: str, model_index:str, temp:float, history:list):
async def generate_answer(data: Generate):
    # a=Request.json()
    # pprint(data)
    # pprint(history)
    
    
    pprint(data.__dict__)
    text=data.text
    model_index=data.model_index
    temp=data.temp
    history=data.history
    isAudio=data.is_audio
    promt=data.promt

    if promt.startswith('https://'):
        promt=gpt.load_prompt(promt)
    else:
        promt=data.promt
    
    pprint(data.__dict__)
    answer, token, price, docs =gpt.answer_index(system=promt, topic=text, history=history, 
                                                 search_index=MODELS_INDEX[model_index],
                                                 temp=temp, verbose=0)
    return {"answer": answer, 'isAudio': isAudio, 'token': token, 'price': price, 'docs': docs}




@app.post("/update_model_index/")
def update_model_index():
    update_or_create_model_index()
    return {"message": "Модель обновлена!"}



# @app.get("/recognition-audio/")
# async def recognition_audio():
    
    
#     fileName='voice/{}.mp3'
#     transcript_audio()
@app.post("/recognition-audio/")
async def upload_audio(userID: str = Form(...), file: UploadFile = File(...)):
    # Проверяем, что файл имеет расширение mp3
    pprint(file.content_type)
    pprint(file.__dict__)
    print(f'{file.filename=}')
    # if file.filename.split('.')[1] != 'opus':
    #     return {"error": "File type not supported. Please upload an opus file."}
    
    # userID=0
    # Сохраняем файл в папку voice/
    file_location = f"voice/{file.filename}"
    with open(file_location, "wb") as audio_file:
        audio_file.write(await file.read())

    # Транскрибируем аудиофайл
    text = transcript_audio(file_location)

    url=f'http://{HANDLER_MESSAGE_URL}/handler_message'
    params={'chat_id':userID, 'text':text, 'messanger':'telegram'}
    
    answer = await request_data(url, params)
    answer_voice_file = gpt.answer_voice(userID=userID, text=answer)
    file_location = answer_voice_file

    async def file_remover():
        try:
            os.remove(file_location)
            print(f"Файл {file_location} успешно удален.")
        except Exception as e:
            print(f"Ошибка при удалении файла {file_location}: {e}")


    return FileResponse(
        path=file_location,
        media_type="audio/mpeg",
        filename=file.filename,
        background=file_remover
    )


    # return {"info": f"File '{file.filename}' saved at '{file_location}'"}


# from fastapi.responses import FileResponse
# @app.get("/generate-audio/{text}/{userID}")
@app.get("/generate-audio/")
async def generate_audio(data: Gen_Audio):
    text=data.text
    userID=data.userID
    answer_voice_file = gpt.answer_voice(userID=userID, text=text)
    answer_voice_file_path = answer_voice_file
    # print(f'{answer_voice_file=}')
    # answer_voice_file=FSInputFile(answer_voice_file)
    
    # os.remove(answer_voice_file_path)
    # Путь к директории с аудиофайлами

    # file_path = Path("audios") / f"{userID}.mp3"
    fileName = f"{userID}.mp3"
    # Проверка существования файла
    # if not answer_voice_file_path.is_file():
    #     return Response(content="File not found", status_code=404)
    
    # Определяем функцию для удаления файла после ответа
    
    async def file_remover():
        try:
            os.remove(answer_voice_file_path)
            print(f"Файл {answer_voice_file_path} успешно удален.")
        except Exception as e:
            print(f"Ошибка при удалении файла {answer_voice_file_path}: {e}")

    # Возвращаем файл с удалением после ответа
    return FileResponse(
        path=answer_voice_file_path,
        background=file_remover
    )
    # return FileResponse(
    #     path=answer_voice_file_path,
    #     media_type="audio/mpeg",
    #     filename=fileName,
    #     background=file_remover
    # )

#работа с логами

def log_counts_by_level(logs: list) -> dict:
    counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    for log in logs:
        counts[log['level']] += 1
    return counts

def log_counts_by_minute(logs: list) -> dict:
    counts_by_minute = {}
    for log in logs:
        timestamp_minute = log['timestamp'][:16]  # Обрезаем до минут
        if timestamp_minute in counts_by_minute:
            counts_by_minute[timestamp_minute][log['level']] += 1
        else:
            counts_by_minute[timestamp_minute] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
            counts_by_minute[timestamp_minute][log['level']] += 1
    return counts_by_minute

@app.post("/logs")
async def add_log(log: Request):
    global logs

    # pprint(log.__dict__)
    json = await log.json()
    log_entry=json.get('log_entry')
    log_level = json.get('log_level')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if len(logs) >= 100:
        logs.pop(0)
    logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
    return {"message": "Лог записан!"}

@app.get("/logs", response_class=HTMLResponse)
async def view_logs(request: Request):
    global logs
    for log in logs:
        if isinstance(log['message'], dict) or isinstance(log['message'], list):
            log['message'] = pformat(log['message'])

    logs.reverse()
    counts_log = log_counts_by_level(logs)
    counts_log = log_counts_by_minute(logs)
    pprint(counts_log)
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs, "log_counts": counts_log})

@app.post("/clear_logs")
async def clear_logs():
    global logs
    logs.clear()
    return {"message": "Логи очищены!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
