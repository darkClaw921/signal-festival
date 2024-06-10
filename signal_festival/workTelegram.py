import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
# import config
from handlers import router

from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('TOKEN')
# PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
session = AiohttpSession()
# Тестирование бота "Афиша"
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    print('[OK]')
    asyncio.run(main())