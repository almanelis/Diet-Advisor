from aiogram import Router
from aiogram.types import Message

from lexicon import LEXICON

router = Router()


# Этот хендлер реагирует на другие сообщения
@router.message()
async def process_other_message(message: Message):
    await message.answer(LEXICON['other_message'])
