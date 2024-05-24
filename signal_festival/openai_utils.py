# openai_utils.py

import os
import re
import httpx
import tiktoken
from loguru import logger
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from openai import OpenAI, AsyncOpenAI
from tokenGenerate import get_iam_token
from langchain_community.chat_models import ChatYandexGPT
from langchain.schema import HumanMessage, SystemMessage
load_dotenv()

# Конфигурация OpenAI API ключа
openai_api_key = os.getenv('OPENAI_API_KEY')
# client = OpenAI(api_key=openai_api_key)
client = AsyncOpenAI(api_key=openai_api_key)

def answer_yandex(self, promt: str, history: list, temp=1):
        messages = [
            {"role": "system", "content": promt},
            # {"role": "user", "content": topic}
            # {"role": "user", "content": context}
        ]
        chat_model = ChatYandexGPT(
            folder_id='b1gt5t65m4lcof8iumpj',
            model_uri='gpt://b1gt5t65m4lcof8iumpj/yandexgpt',
            temperature=0,
            iam_token=get_iam_token()
        )

        messages.extend(history)
        historyPrepare = []
        for i in messages:
            if i['role'] == 'user':
                historyPrepare.append(HumanMessage(i['content']))
            if i['role'] == 'system':
                historyPrepare.append(SystemMessage(i['content']))
        try:
            answer = chat_model(historyPrepare)
        except:
            chat_model.iam_token = get_iam_token()
            answer = chat_model(historyPrepare)

        answerText = answer.content

        return f'{answerText}', 0, 0


async def download_document(doc_id: str) -> str:
    url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

async def generate_gpt4_response(prompt: str, model_version: str = 'gpt-3.5-turbo-16k') -> str:
    response = await client.chat.completions.create(
        model=model_version,
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )
    return response.choices[0].message.content

async def create_embeddings(data: str):
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))

    source_chunks = []
    splitter = CharacterTextSplitter(separator="==========", chunk_size=1024, chunk_overlap=300)

    for chunk in splitter.split_text(data):
        source_chunks.append(Document(page_content=chunk, metadata={}))

    search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings())
    count_token = num_tokens_from_string(' '.join([x.page_content for x in source_chunks]), "cl100k_base")
    logger.info(f'Количество токенов в документе: {count_token}')
    logger.info(f'ЦЕНА запроса: {0.0004 * (count_token / 1000)} $')
    return search_index

async def create_embeddings_from_prompt(prompt: str):
    embeddings = OpenAIEmbeddings()
    return await embeddings.embed_text(prompt)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":
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