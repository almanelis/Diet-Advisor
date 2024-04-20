from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)

from config_data.config import Config, load_config
from .models import Base

# Инициализируем БД
config_db: Config = load_config().db
engine = create_async_engine(f'postgresql+asyncpg://{config_db.db_name}:'
                             f'{config_db.db_password}@'
                             f'{config_db.db_host}:5432/'
                             f'{config_db.db_user}',
                             echo=True)
# Создаём сессион мейкер
session_maker = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


# Функции для создания и сброса таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
