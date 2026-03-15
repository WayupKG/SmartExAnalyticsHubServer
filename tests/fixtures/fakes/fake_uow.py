from typing import Any

from app.shared.application.unit_of_work import IUnitOfWork
from tests.fixtures.fakes.fake_user_repository import FakeUserRepository


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.users = FakeUserRepository()
        self.committed = False

    async def __aenter__(self) -> FakeUnitOfWork:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
