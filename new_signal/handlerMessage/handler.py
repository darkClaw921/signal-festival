from datetime import datetime
from pprint import pprint
from workRedis import add_message_to_history, get_history, clear_history    
import aiohttp
from dotenv import load_dotenv
import os
from googleSheet import parse_google_sheet
from qvest import QuestManager
from postgreWork import get_all_user_ids, add_new_user, add_new_message
import json
import locale
from datetime import datetime

load_dotenv()

PORT_GENERATE_ANSWER=os.getenv('PORT_GENERATE_ANSWER')
IP_SERVER = os.getenv('IP_SERVER')
GENERATE_ANSWER_URL=os.getenv('GENERATE_ANSWER_URL')
SENDER_MESSAGE_URL=os.getenv('SENDER_MESSAGE_URL')
IS_AUDIO=False
QUEST_MANAGER=None
STATES = {}

async def request_data(url, json):
    async with aiohttp.ClientSession() as session:
        if json is None:
            async with session.get(url=url) as response:
                return await response
        async with session.get(url=url,json=json) as response:
            return await response.text()

async def request_data_param(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,params=params) as response:
            return await response.text()
        
async def request_data_generate_answer(url):
    async with aiohttp.ClientSession() as session:
            async with session.post(url=url) as response:
                return response
       
        
async def send_message(chat_id, text, messanger, IS_AUDIO=False):
    async with aiohttp.ClientSession() as session:
        await session.post(f'http://{SENDER_MESSAGE_URL}/send_message/',
                                params={'chat_id': chat_id, 'text': text,
                                    'messanger': messanger, 
                                    'isAudio': str(IS_AUDIO)})
    return 0    


async def handler_in_command(chat_id: int, command: str, messanger: str,):
    global IS_AUDIO,STATES,QUEST_MANAGER
    if command == '/help':
        await send_message(chat_id, 
                           """/start - начало работы\n/clear - очистить историю диалога\n
/startVoice- начать генерировать в голос\n/stopVoice- остановить генерировать в голос\n/reset- перезагрузить модель\n
/quest <название листа в таблице> - собрать квест\n/sends <сообщение> - рассылка всем пользователям""",
                        messanger, IS_AUDIO=False)
    
    elif command == '/startVoice':
        IS_AUDIO=True
        
        await send_message(chat_id,
                            'Режим голосового ответа на вопросы включен. Задайте свой вопрос и я пришлю Вам голосовое сообщение 🎙', 
                            messanger, IS_AUDIO=False)
    
    elif command == '/stopVoice':
        IS_AUDIO=False
        # requests.post(f'http://{SENDER_MESSAGE_URL}/is_voice_generate/False')
        await send_message(chat_id, 
                           'Режим голосового ответа на вопросы выключен. Мне снова придется печатать свои ответы... ⌨️', 
                           messanger, IS_AUDIO=False)  
    
    elif command == '/reset':
        await send_message(chat_id, 'Модель перезагружается...', messanger, IS_AUDIO=False)

        # await aiohttp.request('POST', f'http://{GENERATE_ANSWER_URL}/update_model_index/')
        await request_data_generate_answer(f'http://{GENERATE_ANSWER_URL}/update_model_index/')

        await send_message(chat_id, 'Модель перезагружена', messanger, IS_AUDIO=False)
        # IS_AUDIO=False
        # await msg.answer('Распознавание аудио выключено')
    elif command == '/clear':
        clear_history(chat_id)
        await send_message(chat_id, 'История диалога очищена', messanger, IS_AUDIO=False)
    
    elif command == '/start':
        nicname=messanger.split(' ')[1]
        messanger=messanger.split(' ')[0]

        await send_message(chat_id, 
                           'Привет! Я - комьюнити-менеджер фестиваля "Сигнал". Чем я могу помочь?', 
                           messanger, IS_AUDIO)
        STATES[chat_id] = 'start'
        # messanger
        add_new_user(chat_id, nicname,1)

    elif command.startswith('/quest'):
        
    
        await send_message(chat_id, 'Подождите немонго пока я обновлю данные', messanger, IS_AUDIO=False)
    
        quest=command.replace('/quest','').strip()
        pprint(quest)
        # parsed_data = parse_google_sheet("Квест 1")
        parsed_data, endMessages = parse_google_sheet(quest)
        pprint(parsed_data)
        QUEST_MANAGER = QuestManager(parsed_data,endMessages)
        await send_message(chat_id, 'Данные обновлены', messanger, IS_AUDIO=False)

        return 0
    elif command.startswith('/sends'):
        text=command.replace('/sends','').strip()
        users=get_all_user_ids()

        for count,userID in enumerate(users):
            await send_message(userID, text, messanger, IS_AUDIO=False)
            if count % 50 == 0:
                await send_message(chat_id, f'Отправлено {count} сообщений', messanger, IS_AUDIO=False)
        await send_message(chat_id, f'Рассылка закончена всего отправлено {count} сообщений', messanger, IS_AUDIO=False)
    
    else:
        
        await send_message(chat_id, 'Неизвестная команда', messanger, IS_AUDIO=False)
    
async def process_kvest_question(userID, messanger):
    global QUEST_MANAGER, STATES
    
    
    
    question = QUEST_MANAGER.get_user_quest(userID).get_current_question()
    
    text=f'{question["text"]}\n\nВарианты ответов:\n'
    for index, option in enumerate(question['options']):
        # print(f"{index + 1}. {option['text']} (баллы: {option['points']})")
        # text+=f"{index + 1}. {option['text']} (баллы: {option['points']})\n"
        text+=f"{index + 1}. {option['text']} \n"


    await send_message(userID, text, messanger, IS_AUDIO=False) 
    # answer = int(input("Введите номер ответа: ")) - 1
        # QUEST_MANAGER.answer_question(userID, answer)

    # await state.Form.kvestAnswer.set()
    STATES[userID] = 'kvestAnswer'
    return 0


async def process_kvest_answer(userID, text,messanger):
    global QUEST_MANAGER, STATES
    

    try:
        answer = int(text) - 1
    except:
        answer = 1

    QUEST_MANAGER.answer_question(userID, answer)
        
    if not QUEST_MANAGER.is_user_finished(userID): 
        await process_kvest_question(userID=userID,messanger=messanger)
    else:
        end_message=QUEST_MANAGER.get_user_end_message(userID)
        await send_message(userID, 
                        end_message,
                        messanger, IS_AUDIO=False)
        STATES[userID] = 'start'
    return 0



async def handler_in_message(chat_id: int, text: str, messanger: str,):
    global IS_AUDIO, STATES, QUEST_MANAGER
    add_message_to_history(chat_id,'user', text)
    history = get_history(chat_id)

    if text.lower() == 'квест': 
        QUEST_MANAGER.start_quest(chat_id)
        STATES[chat_id] = 'kvest'
        await process_kvest_question(chat_id, messanger)
        return 0   
    
    if STATES.get(chat_id) == 'kvestAnswer':
        await process_kvest_answer(chat_id, text, messanger)
        return 0

    userID=chat_id
    if len(history) > 10:
        clear_history(chat_id)
        history=history[-2:]
        add_message_to_history(chat_id, 'user', text)
        history = get_history(chat_id) 

    # pprint(msg.content_type)
    # chromaDBwork.query()
    print(text)
    messagesList = [
       {"role": "user", "content": text}
      ]
    # answer = gpt.answer(promtPreparePost,messagesList)
    

    date=datetime.now().strftime("%d %H:%M")
    
    
    promt=('https://docs.google.com/document/d/1J9F110b3UPABPeWd5pFg0mFoR_5s0CZYlMqR0SYF_wA/edit?usp=sharing')
    
    params = {'text':text,'promt': promt, 
              'history': history, 'model_index': 'main', 
              'temp': 0.5, 'verbose': 1,
              'is_audio': IS_AUDIO,
              'userID': userID}
    
    try:
        # answer=await request_data(f'http://{IP_SERVER}:{PORT_GENERATE_ANSWER}/generate-answer', params)
        answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
        # answer, allToken, allTokenPrice, message_content = gpt.answer_index(promt, messText, history, model_index,temp=0.5, verbose=1)
        # answer = gpt.answer(promt, history, 1)
    except:
        history=get_history(userID)[-2:]
        # answer, allToken, allTokenPrice, message_content = gpt.answer_index(promt, messText, history, model_index,temp=0.5, verbose=0)
        # answer = gpt.answer(promt, history, 1)
        # answer=await request_data(f'http://{IP_SERVER}:{PORT_GENERATE_ANSWER}/generate-answer', params)

        answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
        
    
    # answer=answer['answer']
    answer=json.loads(answer)
    # print(type(answer))
    # pprint(answer)
    docs=answer['docs']
    answer=answer['answer']
    
    textDoc=''
    for doc in docs:
        textDoc+=f'{doc["page_content"]}\n'
    pprint(textDoc)
    
    params = {'chat_id': chat_id, 'text': answer, 'messanger': messanger, 'isAudio': IS_AUDIO}
    pprint(params)
    # if messanger != 'site':
        # await send_message(chat_id, answer, messanger, IS_AUDIO)
    await send_message(chat_id, answer, messanger, IS_AUDIO)
    # await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)
    add_message_to_history(chat_id, 'system', textDoc)
    add_message_to_history(chat_id, 'system', answer)
    try: 
        add_new_message(messageID=chat_id, chatID=chat_id, userID=chat_id, text=text, type_chat='user', payload='0')
        add_new_message(messageID=chat_id, chatID=chat_id, userID=chat_id, text=answer, type_chat='system', payload=answer)
    except Exception as e:
        text=f'Ошибка добавления сообщения в базу данных для пользователя {chat_id} {e}'
        await send_message(400923372, text, 'telegram', IS_AUDIO=False)

    # await msg.answer(f"Твой ID: {msg.from_user.id}")
    
    # await msg.answer(answer, parse_mode='Markdown')
    return answer