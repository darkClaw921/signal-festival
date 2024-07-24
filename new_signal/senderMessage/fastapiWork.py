from fastapi import FastAPI, HTTPException,Form,Depends
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
from fastapi.responses import FileResponse
import aiohttp
from workTelegram import send_audio,send_voice_aiogram
# from fastapi import FastAPI, 
# TOKEN_BOT = os.getenv('TOKEN_BOT_EVENT')

app = FastAPI(debug=False)
load_dotenv()
PORT = os.getenv('PORT_SENDER_MESSAGE')
HOST = os.getenv('HOST')
TOKEN_BOT = os.getenv('TOKEN_BOT')
IP_SERVER = os.getenv('IP_SERVER')
GENERATE_ANSWER_URL=os.getenv('GENERATE_ANSWER_URL')
app = FastAPI(
    title="STRANA System API",
    description="Send Message API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Templates(directory="templates")
logs = []

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
async def request_data(url, json):
    async with aiohttp.ClientSession() as session:
        if json is None:
            async with session.get(url=url) as response:
                return response
        else:
            async with session.get(url=url,json=json) as response:
                return response
        
async def request_data_param(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as response:
            return await response.text()

# SEND_VOISE=False

@app.get("/is_voice_generate/{isStart}")
async def is_voice_generate(isStart: bool):
    global SEND_VOISE
    SEND_VOISE=isStart
    return {"message": f"Send voice {isStart}"}


async def voice_generate(text:str, userID:int):
    # URL для запроса
    # url = "http://example.com/audio/12312312"

    # Выполняем GET-запрос
    # response = requests.get(url)
    params={
        'text': text,
        'userID': userID
    }
    pprint(params)
    # response=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-audio', params)
    
    
    url = f"http://{GENERATE_ANSWER_URL}/generate-audio"  # Замените на адрес вашего сервера A
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url,json=params) as response:
            if response.status == 200:
                # Сохраняем файл
                with open(f"voice/{userID}.mp3", 'wb') as f:
                    f.write(await response.read())
                return f"voice/{userID}.mp3"
                # return {"message": "File downloaded successfully"}
    #     # Сохраняем файл
    # with open(f"voice/{userID}.mp3", 'wb') as f:
    #     f.write(await response.read())
    # return {"message": "File downloaded successfully"}
            else:
                return {"error": "File not found"}
    
    # 1/0
    
    
    
    
    # print(f'{"audio":=^60}')
    # # pprint(response.__dict__)
    # audio_data = await response.read()
    # pprint(audio_data)
    # # pprint(content_disposition = response.headers.get('Content-Disposition'))
    # # output_path=''
    # if response.status == 200:
    #     # Получаем имя файла из заголовка Content-Disposition
    #     content_disposition = response.headers.get('Content-Disposition')
    #     if content_disposition:
    #         _, params = aiohttp.multipart.parse_content_disposition(content_disposition)
    #         output_path = params.get('filename', output_path)
        
    #     # Сохраняем файл
    #     with open('voice/'+output_path, 'wb') as f:
    #         while chunk := await response.content.read(1024):  # Читаем по частям (1024 байта)
    #             f.write(chunk)
    #     1/0
    # return 'voice/'+output_path 
    # # Проверяем, успешно ли выполнен запрос
    # if response.status_code == 200:
    #     # Определяем имя файла из заголовков ответа или задаем его вручную
    #     filename = response.headers.get('Content-Disposition', 'downloaded_file').split('filename=')[-1].strip('"')
        
    #     # Сохраняем полученный файл
    #     with open(filename, 'wb') as f:
    #         f.write(response.content)
        
    #     print(f"Файл '{filename}' успешно сохранен.")
    # else:
    #     print(f"Не удалось получить файл. Статус: {response.status_code}")




@app.post('/send_message')
async def send_message(chat_id: int, text: str, messanger: str, isAudio: str):
    # text=text.e('utf-8')
    SEND_VOISE = True if isAudio=='True' else False
    match messanger:
        case 'telegram':
            if SEND_VOISE:
                voice_path=await voice_generate(text, chat_id)
                # 1/0
                # await send_audio(chat_id, voice_path)
                await send_voice_aiogram(chat_id, voice_path)
                return {"message": "Voice send"}
            
            url = f'https://api.telegram.org/bot{TOKEN_BOT}/sendMessage'
            params = {
                'chat_id': chat_id,
                'text': text
            }
            response = requests.post(url, params=params)
            # data = response.json()
            # pprint(data)
            return {'message': 'Message send'}
        
        case 'whatsapp':
            return {"message": "Whatsapp not supported yet"}
        case 'facebook':
            return {"message": "Facebook not supported yet"}
        case 'instagram':
            return {"message": "Instagram not supported yet"}

        case _:
            return {"message": "Unsupported messenger"}
        


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
