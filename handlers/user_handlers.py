from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import get_user, add_user
from lexicon import LEXICON
from filters import IsJSON
from keyboards import create_inline_kb

router = Router()


# Этот хендлер реагирует на команду /start и сохраняет информацию о
# пользователе в БД
@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    user = await get_user(session, message.from_user.id)
    # Если пользователь никогда не использвал бота
    if not user:
        # Сохраняем пользователя в базе данных
        await add_user(session, message.from_user.id)
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
