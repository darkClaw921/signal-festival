# gpt.py

from gpttunnel_utils import gptunnel_chat_completion, gptunnel_create_embeddings, num_tokens_from_messages, insert_newlines
from loguru import logger
import re

class GPT:
    # def __init__(self, model_version: str = 'gpt-3.5-turbo-16k'):
    def __init__(self, model_version: str = 'gpt-4o'):
        self.model_version = model_version

    async def answer(self, system: str, topic: list, temp: int = 1):
        messages = [{"role": "system", "content": system}]
        messages.extend(topic)
        response = await gptunnel_chat_completion(messages, model=self.model_version)
        total_token = response['usage']['total_tokens']
        answer_text = response['choices'][0]['message']['content']
        return answer_text, total_token, 0.002 * (total_token / 1000)

    async def answer_index(self, system: str, topic: str, history: list, search_index, temp: int = 1, verbose: int = 0):
        docs = search_index.similarity_search(topic, k=4)
        message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\nОтрывок документа №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
        system_message = 'Данные, на основании которых нужно продолжить диалог:'
        messages = [{"role": "system", "content": system + f"{system_message} {message_content}"}, {"role": "user", "content": 'Диалог с клиентом, который нужно продолжить:'}]
        messages.extend(history)
        if verbose:
            logger.info(f"{num_tokens_from_messages(messages, 'gpt-3.5-turbo-0301')} токенов использовано на вопрос")
        response = await gptunnel_chat_completion(messages, model=self.model_version)
        total_token = response['usage']['total_tokens']
        answer_text = response['choices'][0]['message']['content']
        if verbose:
            logger.info(f'{total_token} токенов использовано всего (вопрос-ответ).')
            logger.info(f'ЦЕНА запроса с ответом: {0.002 * (total_token / 1000)} $')
            logger.info(f'ОТВЕТ: \n{insert_newlines(answer_text)}')
        return answer_text, total_token, 0.002 * (total_token / 1000), docs

    async def get_summary(self, history: list, prompt_message: str = 'Write a concise summary of the following and CONCISE SUMMARY IN RUSSIAN:', temp: float = 0.3):
        messages = [{"role": "system", "content": prompt_message}]
        messages.extend(history)
        logger.info(f'answer message get_summary {messages}')
        response = await gptunnel_chat_completion(messages, model=self.model_version)
        logger.info(f'{response["usage"]["total_tokens"]=}')
        logger.info(f'{response["usage"]=}')
        answer = response['choices'][0]['message']['content']
        logger.info(answer)
        return {'role': 'user', 'content': answer}
    

