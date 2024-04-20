from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from ..models import Profile


# Функция добавления профиля пользователя
async def add_profile(session: AsyncSession, data: dict, message: Message):
    obj = Profile(
        name=data['name'],
        age=int(data['age']),
        gender=data['gender'],
        weight=int(data['weight']),
        height=int(data['height']),
        user_id=int(message.from_user.id),
    )
    session.add(obj)
    await session.commit()


# Функция получения профиля пользователя
async def get_profile(session: AsyncSession, user_id: int):
    query = select(Profile).where(Profile.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


# Фукция обновления профиля пользователя
async def update_profile(session: AsyncSession, data: dict, user_id: int):
    query = update(Profile).where(Profile.user_id == user_id).values(
        name=data['name'],
        age=int(data['age']),
        gender=data['gender'],
        weight=int(data['weight']),
        height=int(data['height']),
    )
    await session.execute(query)
    await session.commit()


# в delete потребности нет
async def delete_profile(session: AsyncSession, user_id: int):
    ...
