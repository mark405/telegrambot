import sqlite3 as sq
from aiogram import types


def sql_start():
    global base, cur
    base = sq.connect('testbd.db')
    cur = base.cursor()
    if base:
        print('Connected to Data Base')


async def db_search(data:dict, message:types.Message):
    found_data = cur.execute("SELECT specialty, rating, grade, university FROM kpi WHERE initials = ? AND year = ?;",
                           (data['initials'], data['year'])).fetchall()
    if found_data:
        for ret in found_data:
            await message.reply(f'Униіерситет:\n {ret[3]}\n'
                                f'Спеціальність:\n {ret[0]}\n'
                                f'Місце у списку:\n {ret[1]}\n'
                                f'Балл:\n {ret[2]}\n')
    else:
        await message.reply('Ніяких даних не знайдено(\n')
