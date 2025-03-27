from aiogram.filters import Filter
from aiogram.types import Message


class IsClickChat(Filter):
    async def __call__(self, message: Message):
        # is_bot = message.forward_from.id == 118365835
        is_click_chat = message.chat.id != -1002617742941
        return is_click_chat #and is_bot