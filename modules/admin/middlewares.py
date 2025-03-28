from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import ADMINS_ID


class AdminOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: Dict[str, Any]):
        if event.from_user.id in ADMINS_ID:
            return await handler(event, data)