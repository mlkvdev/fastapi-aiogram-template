import secrets

from fastapi import Header
from fastapi.exceptions import HTTPException

from backend.config.settings import settings


def verify_tg_bot_webhook_secret(secret_key: str = Header(alias='X-Telegram-Bot-Api-Secret-Token')):
    if not secrets.compare_digest(secret_key, settings.BOT_WEBHOOK_SECRET):
        raise HTTPException(status_code=403)
