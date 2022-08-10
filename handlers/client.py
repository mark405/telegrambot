from aiogram import types, Dispatcher
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlite_db.sql_operations import db_search


# Class describing all states (lines that need to be entered)
class FSMClient(StatesGroup):
    initials = State()
    year = State()


# /start
async def start(message: types.Message):
    await message.answer('Привіт!\n'
                         'Я MyEntrant Bot\n\n'
                         'З моєю допомогою ти зможеш знайти своє місце у списках на вступ серед усіх ВНЗ України!\n\n'
                         'Якщо виникли питання, звертайся сюди ...\n\n'
                         'Для того щоб почати, натисни кпонку \"/Знайти себе\"\n'
                         'Щоб перезавантажити бота, натисни нопку \"/Рестарт\"', reply_markup=kb_client)


# /help
async def help(message: types.Message):
    await message.answer('Що я можу:... (To-Do)\n'
                         'Якщо виникли питання, звертайся сюди... (To-do)\n'
                         '...')


# starting search, requesting input of name
async def start_search(message: types.Message):
    await FSMClient.initials.set()
    await message.reply('Будь ласка, введіть ПІБ:')


# Loading initials to dict + requesting input of year
async def load_initials(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text[-1] == '.' and len(message.text.split()) == 2 and message.text.split()[1][1] == '.':
            data['initials'] = message.text.lower().strip()
        elif message.text[-1] == '.' and len(message.text.split()) == 3 and message.text.split()[1][-1] == '.':
            data['initials'] = str(message.text.split()[0] + ' ' +
                                   (message.text.split()[1] + message.text.split()[2])).lower().strip()
        elif len(message.text.split()) == 3 and \
                (message.text.split()[1][-1] != '.' or message.text.split()[2][-1] != '.'):
            new_msg = message.text.split()[0] + ' '
            for i in message.text.split()[1:]:
                if i[-1] != '.':
                    new_msg += i + '.'
                else:
                    new_msg += i
            print(new_msg.lower())
            data['initials'] = new_msg.lower().strip()
        else:
            data['initials'] = message.text.lower().strip()

    await FSMClient.next()
    await message.reply('Введіть рік вступу:')


# Loading year to dict
# End of requests
async def load_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = message.text
    await db_search(dict(data), message)
    await state.finish()


# Handlers registration
def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'Рестарт'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(start_search, commands=['ЗнайтиCебе'], state=None)
    dp.register_message_handler(load_initials, state=FSMClient.initials)
    dp.register_message_handler(load_year, state=FSMClient.year)
