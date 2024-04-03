from aiogram import Router
from aiogram.types import message

from lexicon.lexicon import LEXICON

router = Router()


@router.message()
async def process_other_message():
    await message.answer(LEXICON['other_message'])
