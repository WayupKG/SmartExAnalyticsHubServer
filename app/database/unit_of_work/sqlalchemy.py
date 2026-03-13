from typing import TYPE_CHECKING

from app.database.unit_of_work.base import AbstractUnitOfWork

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def __aenter__(self) -> SQLAlchemyUnitOfWork:
        return self

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()
