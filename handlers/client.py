from aiogram import types, Dispatcher


# /start
async def start(message:types.Message):
    await message.answer('Привіт!\n'
                         'Я MyEntrant Bot... (To-Do)')


# /help
async def help(message:types.Message):
    await message.answer('Що я можу:... (To-Do)\n'
                         'Якщо виникли питання, звертайся сюди... (To-do)\n'
                         '...')

# Handlers registration
def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
