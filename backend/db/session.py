from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from backend.config.settings import settings

async_engine = create_async_engine(url=settings.POSTGRES_DSN_ASYNC, echo=False)
sync_engine = create_engine(url=settings.POSTGRES_DSN, echo=False)
SessionLocal = sessionmaker(sync_engine, autocommit=False, autoflush=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@contextmanager
def sync_session():
    session = SessionLocal()
    yield session
    session.close()
