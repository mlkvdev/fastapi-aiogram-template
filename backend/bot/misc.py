import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update
from aiohttp import TCPConnector
from loguru import logger

from backend.bot.middlewares.i18n import i18n_middleware
from backend.config.settings import settings, redis
from .helpers import get_bot_webhook_url
from .middlewares import setup as setup_middlewares
from .routers import router

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def on_startup():
    if settings.DEBUG is False:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != get_bot_webhook_url():
            await bot.set_webhook(
                get_bot_webhook_url(), secret_token=settings.BOT_WEBHOOK_SECRET
            )
    else:
        run_polling()


async def on_shutdown():
    await bot.session.close()
    await aiogram_dispatcher.workflow_data.get("tcp_connector").close()
    logger.info("Bot shut down")


def init_dispatcher():
    dp = Dispatcher(tcp_connector=TCPConnector(loop=asyncio.get_event_loop()), storage=RedisStorage(redis=redis))
    dp.include_router(router)
    setup_middlewares(dp)
    i18n_middleware.setup(dp)
    return dp


aiogram_dispatcher = init_dispatcher()


async def feed_update(update: Update):
    await aiogram_dispatcher.feed_update(bot, update)


async def feed_raw_update(update: dict):
    await aiogram_dispatcher.feed_raw_update(bot, update)


def run_polling():
    asyncio.create_task(aiogram_dispatcher.start_polling(bot, handle_signals=False))
