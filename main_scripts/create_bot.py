from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

strg = MemoryStorage()

TOKEN = '5485775703:AAF34jO0hM7MdDGFxP_ipkuvoPQ8XIdJnQ0'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=strg)
