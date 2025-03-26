from aiogram.filters import Filter
from aiogram.types import Message

from config import DEVICE_NAME


class IsCheck(Filter):
    async def __call__(self, message: Message):
        # is_bot = message.forward_from.id == 118365835
        is_check = DEVICE_NAME in message.text
        return is_check
