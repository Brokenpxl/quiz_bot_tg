import nest_asyncio
nest_asyncio.apply()

import Utils.config as config
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import aiosqlite 
from aiogram import types
import Utils.handlers as handlers
from Utils.handlers import router
import Utils.db as db


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
#API_TOKEN = '7420052672:AAFxJQGoOtMyIAkpX3FMIJQzDOvPqFg8FLk'



# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await db.create_table()
    # Объект бота
    bot = Bot(token=config.API_TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.include_router (router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
      asyncio.run(main())
    except KeyboardInterrupt:
       print('бот остановлен')