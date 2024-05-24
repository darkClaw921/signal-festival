# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gpt import GPT
from openai_utils import download_document, create_embeddings
# from gptTunnel import GPT
# from gpttunnel_utils import download_document, gptunnel_create_embeddings as create_embeddings
# creatr 
app = FastAPI()

class GPTRequest(BaseModel):
    prompt: str

class GPTAnswerRequest(BaseModel):
    system: str
    topic: list[dict]
    temp: int = 1

class GPTAnswerIndexRequest(BaseModel):
    system: str
    topic: str
    history: list[dict]
    temp: int = 1
    verbose: int = 0

class GPTSummaryRequest(BaseModel):
    history: list[dict]
    prompt_message: str = 'Write a concise summary of the following and CONCISE SUMMARY IN RUSSIAN:'
    temp: float = 0.3

gpt_instance = GPT()

@app.get("/download/{doc_id}")
async def download(doc_id: str):
    try:
        document_text = await download_document(doc_id)
        return {"document_text": document_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gpt4")
async def call_gpt4(request: GPTRequest):
    try:
        response = await gpt_instance.answer(system="", topic=[{"role": "user", "content": request.prompt}])
        return {"response": response[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gpt4/answer")
async def gpt4_answer(request: GPTAnswerRequest):
    try:
        response = await gpt_instance.answer(system=request.system, topic=request.topic, temp=request.temp)
        return {"response": response[0], "total_tokens": response[1], "cost": response[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gpt4/answer_index")
async def gpt4_answer_index(request: GPTAnswerIndexRequest):
    try:
        search_index = await create_embeddings(request.topic)
        response = await gpt_instance.answer_index(system=request.system, topic=request.topic, history=request.history, search_index=search_index, temp=request.temp, verbose=request.verbose)
        return {"response": response[0], "total_tokens": response[1], "cost": response[2], "docs": response[3]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gpt4/summary")
async def gpt4_summary(request: GPTSummaryRequest):
    try:
        response = await gpt_instance.get_summary(history=request.history, prompt_message=request.prompt_message, temp=request.temp)
        return {"summary": response['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)