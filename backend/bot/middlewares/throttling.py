from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, User, CallbackQuery
from aiolimiter import AsyncLimiter

from .base import BaseMiddleware


class ThrottlingMiddleware(BaseMiddleware):
    is_outer = False

    def __init__(self, default_rate: int = .3) -> None:
        self.limiters: Dict[str, AsyncLimiter] = {}
        self.default_rate = default_rate

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")
        throttling_flag = get_flag(data["handler"], 'rate_limit')
        if throttling_flag is None:
            throttling_flag = {}
        throttling_key = throttling_flag.get('key', None)
        throttling_rate = throttling_flag.get('rate', self.default_rate)

        if not throttling_key or not user:
            return await handler(event, data)

        limiter = self.limiters.setdefault(
            f"{user.id}:{throttling_key}", AsyncLimiter(1, throttling_rate)
        )
        if limiter.has_capacity():
            async with limiter:
                return await handler(event, data)
        else:
            if isinstance(event, CallbackQuery):
                await event.answer(str("Do not flood. Wait a second!"))
            return None
