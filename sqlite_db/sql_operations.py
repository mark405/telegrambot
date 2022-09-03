import sqlite3 as sq

import aiogram.utils.exceptions
from aiogram import types
from keyboards import kb_client


# Connecting to database
def sql_start():
    global base, cur
    base = sq.connect('entrants.db')
    cur = base.cursor()
    if base:
        print('Connected to Data Base')


# Making request basing on user's initials and year of campaign
# Sending out all requested data
async def db_search(data: dict, message: types.Message):
    years = {'2020': 'ZERO', '2021': 'ONE', '2022': 'TWO'}
    sel = f"SELECT SPECIALITY, NUMBER, SCORE, UNIVERSITY, FACULTY, DEGREE, STATUS, PRIOITY FROM {years[data['year']]} WHERE LOWER(NAME) = ?;"
    found_data = cur.execute(sel,
                             (data['initials'],)).fetchall()
    if found_data:
        for ret in found_data:
            await message.reply(f'Університет:\n {ret[3] if ret[3] != "not" else "Невідомо"}\n\n'
                                f'Факультет: \n {ret[4] if ret[4] != "not" else "Невідомо"}\n\n'
                                f'Диплом:\n {ret[5] if ret[5] != "not" else "Невідомо"}\n\n'
                                f'Спеціальність:\n {ret[0] if ret[0] != "not" else "Невідомо"}\n\n'
                                f'Пріорітет: \n {ret[7] if ret[7] != "not" else "Невідомо"}\n\n'
                                f'Місце у списку:\n {ret[1]}\n\n'
                                f'Балл:\n {ret[2]}\n\n'
                                f'Статус заявки: \n {ret[6]}')
    else:
        await message.reply('Ніяких даних не знайдено(\n', reply_markup=kb_client)
        sel_smlr = f"SELECT NAME FROM {years[data['year']]} WHERE NAME LIKE ?"
        smlr_intls = cur.execute(sel_smlr,
                                 (f"{str(data['initials']).split()[0]}%",)).fetchall()
        if smlr_intls:
            prcst_intls = []
            for i in set(smlr_intls[:25]):
                # prcst_intls.append(
                #     str(i[0].split()[0][0].upper() + i[0].split()[0][1:] + ' ' + i[0].split()[1].upper()))
                prcst_intls.append(i[0])
            outp = 'Можливо, Ви мали на увазі:\n\n'
            for r in prcst_intls:
                outp += str(r + '\n')
            try:
                await message.answer(outp)
            except aiogram.utils.exceptions.MessageIsTooLong:
                pass
