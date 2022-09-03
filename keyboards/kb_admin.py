from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b_rfl = KeyboardButton('/Оновити')
b_chck = KeyboardButton('/Статус')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(b_rfl, b_chck)