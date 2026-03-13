from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.pool import Pool


@dataclass
class HelperParams:
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    poolclass: type[Pool] | None = None


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        params: HelperParams,
    ) -> None:
        engine_kwargs: dict[str, bool | int | type[Pool]] = {
            "echo": params.echo,
            "echo_pool": params.echo_pool,
        }

        if params.poolclass:
            engine_kwargs["poolclass"] = params.poolclass
        else:
            engine_kwargs.update(
                pool_size=params.pool_size,
                max_overflow=params.max_overflow,
            )

        self.engine: AsyncEngine = create_async_engine(url, **engine_kwargs)

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    params=HelperParams(
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    ),
)
