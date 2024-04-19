import logging

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config_data.config import Config, load_config
from database.engine import create_db, session_maker
from handlers import other_handlers, user_handlers, user_form_handlers
from keyboards import set_main_menu
from middlewares.db import DataBaseSession

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')

    # Инициализируем Redis
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    
    # Создаём БД
    await create_db()

    # Настраиваем главное меню бота
    await set_main_menu(bot)
    # Регистрация middleware в диспетчере
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(user_form_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
