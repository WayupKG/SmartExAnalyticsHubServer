from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.orm_base import Base
from app.shared.infrastructure.orm_mixins import (
    ActionDataTimeMixin,
    BaseIDMixin,
)
from app.users.domain.entities import UserEntity
from app.users.domain.enums import UserRole


class UserModel(Base, BaseIDMixin, ActionDataTimeMixin):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(
        String(70),
        unique=True,
        index=True,
    )
    role: Mapped[UserRole] = mapped_column(
        String(50),
        default=UserRole.MARKETER,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            hashed_password=self.hashed_password,
            role=self.role,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
