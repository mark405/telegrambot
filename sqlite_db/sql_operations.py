import sqlite3 as sq
from aiogram import types


# Connecting to database
def sql_start():
    global base, cur
    base = sq.connect('test.db')
    cur = base.cursor()
    if base:
        print('Connected to Data Base')


# Making request basing on user's initials and year of campaign
# Sending out all requested data
async def db_search(data: dict, message: types.Message):
    years = {'2020': 'ZERO', '2021': 'ONE', '2022': 'TWO'}
    print(years[data['year']])
    sel = f"SELECT SPECIALITY, NUMBER, SCORE, UNIVERSITY, FACULTY, DEGREE, STATUS, PRIOITY FROM {years[data['year']]} WHERE LOWER(NAME) = ?;"
    found_data = cur.execute(sel,
                             (data['initials'], )).fetchall()
    if found_data:
        for ret in found_data:
            await message.reply(f'Університет:\n {ret[3]}\n'
                                f'Факультет: \n {ret[4]}\n'
                                f'Диплом:\n {ret[5]}\n'
                                f'Спеціальність:\n {ret[0]}\n'
                                f'Пріорітет: \n {ret[7]}\n'
                                f'Місце у списку:\n {ret[1]}\n'
                                f'Балл:\n {ret[2]}\n'
                                f'Статус заявки: \n {ret[6]}')
    else:
        await message.reply('Ніяких даних не знайдено(\n')
        sel_smlr = f"SELECT NAME FROM {years[data['year']]} WHERE NAME LIKE ?"
        smlr_intls = cur.execute(sel_smlr,
                                 (f"{str(data['initials']).split()[0]}%", )).fetchall()
        print(set(smlr_intls))
        if smlr_intls:
            prcst_intls = []
            for i in set(smlr_intls):
                prcst_intls.append(
                    str(i[0].split()[0][0].upper() + i[0].split()[0][1:] + ' ' + i[0].split()[1].upper()))
            outp = 'Можливо, Ви мали на увазі:\n\n'
            for ret in prcst_intls:
                outp += str(ret + '\n')
            await message.answer(outp)
