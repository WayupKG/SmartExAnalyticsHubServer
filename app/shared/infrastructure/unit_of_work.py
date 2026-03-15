from typing import TYPE_CHECKING, Any

from app.shared.application.unit_of_work import IUnitOfWork
from app.users.infrastructure.repositories import UserRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SQLAlchemyUnitOfWork(IUnitOfWork):
    """
    Реализация UnitOfWork для SQLAlchemy.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | None = None,
        session_override: AsyncSession | None = None,
    ):
        self.session_factory = session_factory
        self.session_override = session_override
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> SQLAlchemyUnitOfWork:
        if self.session_override:
            self.session = self.session_override
        elif self.session_factory:
            self.session = self.session_factory()
        else:
            raise ValueError("Не передан ни session_factory, ни session_override")

        self.users = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session and not self.session_override:
            if exc_type:
                await self.session.rollback()
            await self.session.close()

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
