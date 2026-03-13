from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.orm_base import Base
from app.shared.infrastructure.orm_mixins import ActionDataTimeMixin, UUIDMixin


class UserORM(Base, UUIDMixin, ActionDataTimeMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
