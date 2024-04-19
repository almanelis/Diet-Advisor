import os 

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config_data.config import Config, load_config
from .models import Base

# Инициализируем БД
config: Config = load_config()
engine = create_async_engine(config.db.db_lite, echo=True)
# Создаём сессион мейкер
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Функции для создания и сброса таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
