import sqlite3 as sq
from aiogram import types


# Connecting to database
def sql_start():
    global base, cur
    base = sq.connect('testbd.db')
    cur = base.cursor()
    if base:
        print('Connected to Data Base')


# Making request basing on user's initials and year of campaign
# Sending out all requested data
async def db_search(data: dict, message: types.Message):
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
        smlr_intls = cur.execute("SELECT initials FROM kpi WHERE initials LIKE ?;",
                                 (f"{str(data['initials'][:4])}%", )).fetchall()
        print(smlr_intls)
        if smlr_intls:
            prcst_intls = []
            for i in set(smlr_intls):
                prcst_intls.append(
                    str(i[0].split()[0][0].upper() + i[0].split()[0][1:] + ' ' + i[0].split()[1].upper()))
            outp = 'Можливо, Ви мали на увазі:\n\n'
            for ret in prcst_intls:
                outp += str(ret + '\n')
            await message.answer(outp)
