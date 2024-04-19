from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from lexicon import LEXICON
from filters import IsJSON
from keyboards import create_inline_kb

router = Router()


# Этот хендлер реагирует на команду /start и сохраняет информацию о
# пользователе в БД
@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    # Сохраняем пользователя в базе данных
    session.add(User(
        tg_id=message.from_user.id,
    ))
    await session.commit()

    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(LEXICON[message.text],
                         reply_markup=reply_markup)


# Этот хэндлер реагирует на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хендлер временно реагирует на .json файлы
@router.message(IsJSON())
async def process_json(message: Message):
    await message.answer(message.document.file_name + LEXICON['json_received'])
