import aiogram.types.reply_keyboard
from aiogram import types, Dispatcher
from keyboards import kb_client
from keyboards.kb_admin import kb_admin
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlite_db.sql_operations import db_search
from adm_id.admins_ids import adm_ids
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Class describing all states (lines that need to be entered)
class FSMClient(StatesGroup):
    initials = State()
    year = State()


# /start
async def start(message: types.Message):
    uid = await get_user_id(message)
    if uid not in adm_ids:
        await message.answer('Привіт!\n'
                             'Я MyEntrant Bot\n\n'
                             'З моєю допомогою ти зможеш знайти свої дані у списках на вступ серед усіх ВНЗ України!'
                             '\n\n'
                             'Для того щоб почати, натисни кпонку \"/Знайти себе\"\n'
                             'Щоб перезавантажити бота, натисни нопку \"/Рестарт\"', reply_markup=kb_client)
    else:
        await message.answer('Hello admin', reply_markup=kb_admin)


# /help
async def help(message: types.Message):
    await message.answer('Інструкція з використання:\n'
                         'ПІБ можна вводити тільки з першою великою літерою.\n'
                         'Ім\'я по-батькові мають бути обов\'язково з двома великими літерами. '
                         'Крапки мають стояти після кожної з літер ініціалів.'
                         '\n\n'
                         'Приклад правильного введення:\n'
                         'Іванов А.Б. (не іванов а.б., Іванов А Б, іванов а б, іванов тощо)'
                         '\n\n'
                         'Наразі бот підтримує пошук по усіх абітурєнтах за 2020, 2021 та 2022 роки.\n'
                         'Усі дані беруться з сайту abit-help: https://abit-help.com.ua/'
                         '\n\n'
                         'Іноді з технічних причин дані бота можуть \"відставати\" від даних з сайту. Ми працюємо над цим)'
                         '\n\n'
                         'Якщо виникли питання або побажання, будемо раді слухати вас тут: @pasha_sandman @zavgod\n\n'
                         'Приємного користування!)', reply_markup=kb_client)


# starting search, requesting input of name
async def start_search(message: types.Message):
    await FSMClient.initials.set()
    await message.reply('Будь ласка, введіть ПІБ:')


# Loading initials to dict + requesting input of year
async def load_initials(message: types.Message, state: FSMContext):
    aiogram.types.reply_keyboard.ReplyKeyboardRemove(kb_client)
    async with state.proxy() as data:
    # To Be Updated

        # try:
        #     if message.text[-1] == '.' and len(message.text.split()) == 2 and message.text.split()[1][1] == '.':
        #         data['initials'] = message.text.lower().strip()
        #
        #     elif message.text[-1] == '.' and len(message.text.split()) == 3 and message.text.split()[1][-1] == '.':
        #         data['initials'] = str(message.text.split()[0] + ' ' +
        #                                (message.text.split()[1] + message.text.split()[2])).lower().strip()
        #
        #     elif len(message.text.split()) == 3 and \
        #             (message.text.split()[1][-1] != '.' or message.text.split()[2][-1] != '.') or \
        #             (message.text.split()[1][-1] != '.' and message.text.split()[2][-1] != '.'):
        #         new_msg = message.text.split()[0] + ' '
        #         for i in message.text.split()[1:]:
        #             if i[-1] != '.':
        #                 new_msg += i + '.'
        #             else:
        #                 new_msg += i
        #         print(new_msg.lower())
        #         data['initials'] = new_msg.lower().strip()
        #
        #     else:
        #         data['initials'] = message.text.lower().strip()
        # except IndexError:
        #     data['initials'] = message.text.lower().strip()

        if message.text[0] == '/':
            await state.finish()
            return
        data['initials'] = message.text

    await FSMClient.next()
    global years_kb
#   Initializing buttons
    b_zero = KeyboardButton('2020')
    b_one = KeyboardButton('2021')
    b_two = KeyboardButton('2022')
    years_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    years_kb.row(b_two).row(b_one).row(b_zero)

    await message.reply('Будь ласка, оберіть рік вступу:', reply_markup=years_kb)


# Loading year to dict
# End of requests
async def load_year(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await state.finish()
        return
    async with state.proxy() as data:
        if message.text in ['2020', '2021', '2022']:
            data['year'] = message.text
        else:
            await message.answer('Такий рік не підтримується ботом(\n'
                                 'Будь ласка, введіть інший рік (2020, 2021 або 2022):', reply_markup=years_kb)
            await FSMClient.last()
            return
    await db_search(dict(data), message)
    await state.finish()
    await message.answer('Щоб знайти іншу людину, натисни кпонку \"/Знайти себе\"\n', reply_markup=kb_client)


async def get_user_id(message:types.Message):
    return message.from_user.id


# Handlers registration
def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'Рестарт'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(start_search, commands=['ЗнайтиCебе'], state=None)
    dp.register_message_handler(load_initials, state=FSMClient.initials)
    dp.register_message_handler(load_year, state=FSMClient.year)
    dp.register_message_handler(get_user_id)
