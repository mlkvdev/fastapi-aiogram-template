from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Chat

from .base import BaseMiddleware


class UserMiddleware(BaseMiddleware):
    is_outer = False

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        allow_any = get_flag(data["handler"], 'allow_any')
        bot: Bot = data['bot']
        chat: Chat = data['event_chat']
        if not allow_any:
            pass
        return await handler(event, data)
