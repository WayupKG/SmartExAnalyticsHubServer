from abc import ABC, abstractmethod
from typing import TypeVar

TUnitOfWork = TypeVar("TUnitOfWork", bound="AbstractUnitOfWork")


class AbstractUnitOfWork(ABC):
    """
    Интерфейс для Unit of Work, инкапсулирующий управление транзакцией.
    """

    async def __aenter__(self: TUnitOfWork) -> TUnitOfWork:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
