from typing import TYPE_CHECKING

from app.users.application.interfaces import IUserRepository

if TYPE_CHECKING:
    from app.users.domain.entities import User


class FakeUserRepository(IUserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    async def get_by_email(self, email: str) -> User | None:
        return self._users.get(email)

    async def save(self, user: User) -> None:
        self._users[user.email] = user
