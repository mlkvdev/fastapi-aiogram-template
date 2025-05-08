from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject


class BaseMiddleware:
    is_outer = False

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        raise NotImplementedError
