from typing import Dict, Any

from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware as BaseI18nMiddleware

from backend.bot.translation import i18n


class I18nMiddleware(BaseI18nMiddleware):

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user: User = data.get('event_from_user')
        return user.language_code


i18n_middleware = I18nMiddleware(i18n)
