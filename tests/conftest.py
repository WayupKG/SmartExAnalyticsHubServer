import os
from typing import TYPE_CHECKING

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.orm import Session, SessionTransaction
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import DatabaseHelper, HelperParams, db_helper
from app.main import main_app
from app.shared.infrastructure.orm_base import Base

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


def get_test_db_url() -> str:
    """Генерирует уникальный URL БД для каждого воркера xdist."""
    base_url = str(settings.db_test.url)
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")

    if worker_id:
        # Изменяем имя базы: test_db -> test_db_gw0, test_db_gw1
        if "?" in base_url:
            url_part, query_part = base_url.split("?")
            return f"{url_part}_{worker_id}?{query_part}"
        return f"{base_url}_{worker_id}"
    return base_url


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def test_db_helper() -> AsyncGenerator[DatabaseHelper]:
    """
    Создает экземпляр DatabaseHelper специально для тестов.
    """
    helper = DatabaseHelper(
        url=str(settings.db_test.url),
        params=HelperParams(
            echo=False,
            pool_size=0,
            max_overflow=0,
            poolclass=NullPool,
        ),
    )

    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield helper

    await helper.dispose()


@pytest_asyncio.fixture(scope="function")
async def connection(
    test_db_helper: DatabaseHelper,
) -> AsyncGenerator[AsyncConnection]:
    """Обеспечивает чистую транзакцию для каждого теста."""
    conn = await test_db_helper.engine.connect()
    trans = await conn.begin()

    yield conn

    await trans.rollback()
    await conn.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_dependencies(
    db_session: AsyncSession,
    test_db_helper: DatabaseHelper,
) -> AsyncGenerator[None]:

    async def _get_test_session() -> AsyncGenerator[AsyncSession]:
        yield db_session

    main_app.dependency_overrides[db_helper.session_getter] = _get_test_session
    main_app.state.db_session_factory = test_db_helper.session_factory

    yield

    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def db_session(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession]:
    """
    Создает сессию. Любой commit() в коде приложения будет перехвачен
    вложенным savepoint-ом и не изменит состояние БД реально.
    """
    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    @event.listens_for(session.sync_session, "after_transaction_end")
    def restart_savepoint(
        sync_session: Session,
        transaction: SessionTransaction,
    ) -> None:
        """
        Исправленная версия слушателя с проверкой на None для MyPy.
        """
        if transaction.nested:
            parent = transaction.parent
            if parent is not None and not parent.is_active:
                return

        # Перезапускаем вложенную транзакцию, если она не активна
        if not sync_session.in_nested_transaction():
            sync_session.begin_nested()

    yield session

    await session.close()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient]:
    """Асинхронный клиент для интеграционных тестов API."""
    transport = ASGITransport(app=main_app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as ac:
        yield ac
