import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api import router
from backend.bot.misc import on_shutdown, on_startup
from backend.config.settings import redis, settings
from backend.db.session import async_session

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(*args, **kwargs):
    settings.LOCALE_DIR.mkdir(exist_ok=True, parents=True)
    await on_startup()
    yield
    await on_shutdown()
    await redis.close()
    await async_session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
