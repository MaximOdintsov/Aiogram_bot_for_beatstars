from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from other.database import API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
