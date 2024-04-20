from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User


# Функция добавления нового пользователя
async def add_user(session: AsyncSession, tg_id: int):
    obj = User(tg_id=tg_id)
    session.add(obj)
    await session.commit()


# Функция получения профиля пользователя
async def get_user(session: AsyncSession, tg_id: int):
    query =  select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()
