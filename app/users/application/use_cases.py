from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.shared.infrastructure.security import hash_password
from app.users.domain.entities import UserEntity
from app.users.domain.enums import UserRole
from app.users.domain.exceptions import EmailAlreadyExistsError

if TYPE_CHECKING:
    from app.shared.application.unit_of_work import IUnitOfWork
    from app.users.presentation.schemas import UserCreateSchema


@dataclass
class RegisterUserUseCase:
    uow: IUnitOfWork

    async def execute(self, user_in: UserCreateSchema) -> UserEntity:
        async with self.uow:
            existing_user = await self.uow.users.get_by_email(user_in.email)
            if existing_user:
                raise EmailAlreadyExistsError()

            user = UserEntity(
                first_name=user_in.first_name,
                last_name=user_in.last_name,
                email=user_in.email,
                hashed_password=hash_password(user_in.password),
                role=UserRole.MARKETER,
            )

            await self.uow.users.save(user)
            await self.uow.commit()

            return user
