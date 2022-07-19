import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from database import API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)