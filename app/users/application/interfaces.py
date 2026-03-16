from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.users.domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity | None:
        pass
