from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Chat, ReplyKeyboardRemove
from loguru import logger

from backend.bot import constants
from backend.db.models import TelegramUser
from backend.utils.uzmeter.exceptions import UnauthorizedHttpException, UZMeterException
from .base import BaseMiddleware


class UserMiddleware(BaseMiddleware):
    is_outer = False

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        allow_any = get_flag(data["handler"], 'allow_any')
        user_obj: TelegramUser = data.get('user_obj')
        bot: Bot = data['bot']
        chat: Chat = data['event_chat']
        if not allow_any:
            if user_obj is None or not user_obj.is_authenticated:
                await bot.send_message(chat.id, str(constants.REGISTER_FIRST),
                                       reply_markup=ReplyKeyboardRemove())
                return False
        try:
            return await handler(event, data)
        except UnauthorizedHttpException:
            await user_obj.delete_token()
            await bot.send_message(chat.id, str(constants.REGISTER_FIRST), reply_markup=ReplyKeyboardRemove())
        except UZMeterException as e:
            await bot.send_message(chat.id, str(constants.ERROR_OCCURRED_CONTACT_TO_ADMIN))
            logger.error(e)
