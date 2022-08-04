from aiogram import types, Dispatcher
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlite_db.sql_operations import db_search

class FSMClient(StatesGroup):
    initials = State()
    year = State()

# /start
async def start(message:types.Message):
    await message.answer('Привіт!\n'
                         'Я MyEntrant Bot... (To-Do)', reply_markup=kb_client)


# /help
async def help(message:types.Message):
    await message.answer('Що я можу:... (To-Do)\n'
                         'Якщо виникли питання, звертайся сюди... (To-do)\n'
                         '...')


# starting search, requesting input of name
async def start_search(message:types.Message):
    await FSMClient.initials.set()
    await message.reply('Будь ласка, введіть ПІБ:')


# Loading initials to dict + requesting input of year
async def load_initials(message:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['initials'] = message.text
    await FSMClient.next()
    await message.reply('Введіть рік вступу:')


# Loading year to dict and ending search
async def load_year(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['year'] = message.text
    await db_search(dict(data), message)
    await state.finish()


# Handlers registration
def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(start_search, commands=['ЗнайтиCебе'], state=None)
    dp.register_message_handler(load_initials, state=FSMClient.initials)
    dp.register_message_handler(load_year, state=FSMClient.year)
