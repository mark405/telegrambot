import asyncio
import threading

from aiogram import types, Dispatcher
from parser.parser import refill
from adm_id.admins_ids import adm_ids


endcd = []


async def refill_db(message:types.Message):
    if message.from_user.id not in adm_ids:
        await message.answer('Ви не маєте доступу до використання цієї фнкції.')
        return
    await message.answer('Починаю оновлення...')
    t = threading.Thread(target=asyncio.run, args=(refill(endcd), ))
    t.start()


async def check(message:types.Message):
    if message.from_user.id not in adm_ids:
        await message.answer('Ви не маєте доступу до використання цієї фнкції.')
        return
    if len(endcd) > 0:
        await message.answer('Оновлення закінчено')
        endcd.clear()
    else:
        await message.answer('Оновлення триває')


def reg_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(refill_db, commands=['Оновити'])
    dp.register_message_handler(check, commands=['Статус'])
