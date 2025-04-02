from aiogram.filters import Filter
from aiogram.types import Message


class IsClickChat(Filter):
    async def __call__(self, message: Message):
        try:
            is_bot = message.forward_from.id == 118365835
            is_click_chat = message.chat.id == -1002560974644

            return is_click_chat and 'Аппарат' in message.text and is_bot
        except Exception as e:
            print(e)
            return False
