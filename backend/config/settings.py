from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from redis.asyncio import from_url

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')
    DEBUG: bool = True
    BOT_TOKEN: str
    BOT_WEBHOOK_SECRET: str
    REDIS_URL: str
    POSTGRES_DSN: str
    POSTGRES_DSN_ASYNC: str
    LOCALE_DIR: Path = BASE_DIR.parent / 'locales'
    BASE_URL: str

settings = Settings(_env_file=BASE_DIR.parent / ".env")
redis = from_url(settings.REDIS_URL)
