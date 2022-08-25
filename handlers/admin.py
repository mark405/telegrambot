from aiogram import types, Dispatcher
from parser.parser import refill


async def refill_db(message:types.Message):
    await message.answer('Починаю оновлення...')
    await refill()
    await message.answer('Оновлення завершено')


def reg_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(refill_db, commands=['Оновити'])