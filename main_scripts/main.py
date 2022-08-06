from aiogram.utils import executor
from create_bot import dp
from handlers import client
from sqlite_db import sql_operations


# Printing out and connecting to database everytime bot starts up
async def startup(_):
    sql_operations.sql_start()
    print('Bot is online')

# Registration of all handlers in main
client.reg_handlers_client(dp)

executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=startup)
