from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])
