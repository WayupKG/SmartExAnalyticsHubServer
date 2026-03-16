from typing import TYPE_CHECKING

from app.users.application.interfaces import IUserRepository

if TYPE_CHECKING:
    from app.users.domain.entities import UserEntity


class FakeUserRepository(IUserRepository):
    def __init__(self) -> None:
        self._users: dict[str, UserEntity] = {}

    async def get_by_email(self, email: str) -> UserEntity | None:
        return self._users.get(email)

    async def save(self, user: UserEntity) -> None:
        self._users[user.email] = user
