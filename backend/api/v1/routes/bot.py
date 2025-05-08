from fastapi import APIRouter, Depends, BackgroundTasks
from loguru import logger

from backend.api.v1.deps import verify_tg_bot_webhook_secret
from backend.bot.misc import feed_raw_update

router = APIRouter()


async def __feed_raw_update(update: dict):
    try:
        await feed_raw_update(update)
    except Exception as e:
        logger.exception(e)


@router.post('/webhook', dependencies=[Depends(verify_tg_bot_webhook_secret)])
async def bot_webhook(update: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(__feed_raw_update, update)
    return {'ok': True}
