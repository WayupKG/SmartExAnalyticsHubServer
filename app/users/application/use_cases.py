from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.users.domain.entities import User
from app.users.domain.exceptions import EmailAlreadyExistsError

if TYPE_CHECKING:
    from app.shared.application.unit_of_work import IUnitOfWork


@dataclass
class RegisterUserUseCase:
    uow: IUnitOfWork

    async def execute(self, email: str, password: str) -> User:
        async with self.uow:
            # 1. Проверяем через репозиторий, привязанный к UoW
            existing_user = await self.uow.users.get_by_email(email)
            if existing_user:
                raise EmailAlreadyExistsError("Email уже занят")

            user = User(email=email, hashed_password=password + "_hash")
            await self.uow.users.save(user)

            await self.uow.commit()

            return user
