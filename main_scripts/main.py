from aiogram.utils import executor
from create_bot import dp
from handlers import client


# Printing out everytime bot starts up
async def startup(_):
    print('Bot is online')

# Registrating all handlers in main
client.reg_handlers_client(dp)

executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=startup)

