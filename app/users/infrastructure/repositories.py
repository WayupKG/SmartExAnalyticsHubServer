from dataclasses import asdict

from app.shared.domain.enums import Op
from app.shared.domain.filters import Condition
from app.shared.infrastructure.repositories import SQLAlchemyRepository
from app.users.application.interfaces import IUserRepository
from app.users.domain.entities import User
from app.users.infrastructure.orm_models import UserORM


class UserRepository(SQLAlchemyRepository[UserORM], IUserRepository):
    model = UserORM

    @staticmethod
    def _to_domain(orm_model: UserORM) -> User:
        """Вспомогательный метод маппинга"""
        return User(
            id=orm_model.id,
            email=orm_model.email,
            hashed_password=orm_model.hashed_password,
            is_active=orm_model.is_active,
        )

    async def get_by_email(self, email: str) -> User | None:
        condition = Condition(field="email", op=Op.EQ, value=email)

        orm_model = await self.get_one(filters=condition)

        if not orm_model:
            return None

        return self._to_domain(orm_model)

    async def save(self, user: User) -> None:
        user_data = asdict(user)
        user_orm = UserORM(**user_data)
        await self.add(user_orm)
