import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import FSInputFile
# import config
# from handlers import router
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types 

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN_BOT')


async def send_audio(userID:int,filePath:str):
    # bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = telebot.TeleBot(TOKEN)
    bot.send_voice(userID, filePath)
    # await bot.send_audio(chat_id=userID, audio=filePath)
    os.remove(filePath)
    return 0

async def send_voice_aiogram(userID:int,filePath:str):
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print(f'filePath: {filePath}')
    answer_voice_file=FSInputFile(filePath)
    await bot.send_voice(userID, voice=answer_voice_file)
    os.remove(filePath)
    return 0
if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    print('[OK]')
    asyncio.run(main())