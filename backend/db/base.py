from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import DateTime, func, BigInteger, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow():
    return datetime.now(UTC)


def gen_uuid4():
    return uuid4()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, server_default=func.now(),
                                                 onupdate=func.current_timestamp())

    @classmethod
    async def create(cls, session: AsyncSession, instance: "Base"):
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def filter(
            cls, session: AsyncSession, *filters, single=False,
            include_count=False, options: list = None,
            page: int = 1,
            page_size: int = 10
    ):
        query = select(cls)

        if filters:
            query = query.where(*filters)

        if single is False:
            if options:
                query = query.options(*options)

            query = query.offset((page - 1) * page_size).limit(page_size).order_by(cls.id.desc())

        result = await session.execute(query)

        if single:
            return result.scalar()

        result = result.scalars().all()

        if include_count:
            count = (await session.execute(select(func.count()).select_from(cls))).scalar()
            return dict(total=count, results=result)

        return result

    @classmethod
    async def delete(cls, session: AsyncSession, *filters):
        if not filters:
            raise ValueError("At least one filter must be provided")
        query = delete(cls).where(*filters)
        await session.execute(query)
        await session.commit()
