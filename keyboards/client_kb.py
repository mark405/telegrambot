from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b_hlp = KeyboardButton('/help')
b_srch = KeyboardButton('/ЗнайтиCебе')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b_hlp, b_srch)
