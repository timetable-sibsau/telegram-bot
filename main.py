import logging
import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, DB_FILE, FILE_LOGGING_MODE
from tinydb import TinyDB, Query


storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(bot, loop=loop, storage=storage)
if FILE_LOGGING_MODE:
    logging.basicConfig(filename='bot.log', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# data-base
db = TinyDB(DB_FILE)
User = Query()


if __name__ == '__main__':
    from handlers import dp, notify_admin, bye_admin
    executor.start_polling(dp, on_startup=notify_admin, on_shutdown=bye_admin, skip_updates=True)
