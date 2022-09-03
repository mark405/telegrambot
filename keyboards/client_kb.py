from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b_rstrt = KeyboardButton('/Рестарт')
b_hlp = KeyboardButton('/help')
b_srch = KeyboardButton('/ЗнайтиCебе')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.row(b_hlp, b_srch, b_rstrt)
