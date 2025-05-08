from fastapi import APIRouter

from .routes.bot import router as bot_router

router = APIRouter()
router.include_router(bot_router, prefix='/bot')
