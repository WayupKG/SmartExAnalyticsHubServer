from dataclasses import asdict
from typing import TYPE_CHECKING

from app.shared.domain.enums import Op
from app.shared.domain.filters import Condition
from app.shared.infrastructure.repositories import SQLAlchemyRepository
from app.users.application.interfaces import IUserRepository
from app.users.infrastructure.orm_models import UserModel

if TYPE_CHECKING:
    from app.users.domain.entities import UserEntity


class UserRepository(SQLAlchemyRepository[UserModel], IUserRepository):
    model = UserModel

    async def get_by_email(self, email: str) -> UserEntity | None:
        condition = Condition(field="email", op=Op.EQ, value=email)
        orm_model = await self.get_one(filters=condition)

        if not orm_model:
            return None
        return orm_model.to_entity()

    async def save(self, user: UserEntity) -> UserEntity | None:
        user_data = asdict(user)
        user_orm = UserModel(**user_data)
        orm_model = await self.add(user_orm)
        return orm_model.to_entity()
