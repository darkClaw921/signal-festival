# gpttunnel_utils.py

import os
import httpx
from dotenv import load_dotenv
import tiktoken
from pprint import pprint
load_dotenv()

# Конфигурация API ключа GPTunnel
gptunnel_api_key = os.getenv('GPTUNNEL_API_KEY')

async def download_document(doc_id: str) -> str:
    url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
    
async def gptunnel_chat_completion(messages: list, model: str = 'gpt-4o'):
    headers = {
        'Authorization': f'{gptunnel_api_key}',
        # 'Authorization': f'Bearer {gptunnel_api_key}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': model,
        'messages': messages,
    }
    pprint(json_data)
    async with httpx.AsyncClient() as client:
        response = await client.post('https://gptunnel.ru/v1/chat/completions', headers=headers, json=json_data)
        pprint(response.text)
        # response.raise_for_status()
        return response.json()

async def gptunnel_create_embeddings(input_text: str, model: str = 'text-embedding-ada-002'):
    headers = {
        'Authorization': f'{gptunnel_api_key}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': model,
        'input': input_text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post('https://gptunnel.ru/v1/embeddings', headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()

def num_tokens_from_messages(messages, model="gpt-4o"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-4o":
        num_tokens = 0
        for message in messages:
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += -1
        num_tokens += 2
        return num_tokens
    else:
        raise NotImplementedError(f"num_tokens_from_messages() is not presently implemented for model {model}.")

def insert_newlines(text: str, max_len: int = 170) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_len:
            lines.append(current_line)
            current_line = ""
        current_line += " " + word
    lines.append(current_line)
    return "\n".join(lines)

if __name__ == '__main__':
    import requests
    from pprint import pprint
    headers = {
        'Authorization': f'{gptunnel_api_key}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://gptunnel.ru/v1/models', headers=headers)
    pprint(response.text)