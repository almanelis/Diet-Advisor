from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from filters.filters import IsJSON
from keyboards.keyboards import create_inline_kb

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    reply_markup = create_inline_kb(1, 'btn_user_form')
    await message.answer(LEXICON[message.text],
                         reply_markup=reply_markup)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(IsJSON())
async def process_json(message: Message):
    await message.answer(message.document.file_name + LEXICON['json_received'])
