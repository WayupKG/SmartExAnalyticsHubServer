import uuid

from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.shared.infrastructure.utils.id_generator import CustomID


class BaseIDMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class CustomIDMixin:
    _id_prefix: str = "abs_"
    _id_length: int = 22

    @declared_attr
    def id(cls) -> Mapped[str]:
        return mapped_column(
            primary_key=True,
            default=CustomID(
                prefix=cls._id_prefix,
                length=cls._id_length,
            ),
        )
