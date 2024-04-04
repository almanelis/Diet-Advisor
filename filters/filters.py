from aiogram.filters import BaseFilter
from aiogram.types import Message


# Фильтр json фалов
class IsJSON(BaseFilter):
    async def __call__(self, message: Message):
        if message.document:
            return message.document.file_name.endswith('.json')
