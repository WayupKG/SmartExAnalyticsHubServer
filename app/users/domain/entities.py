from dataclasses import dataclass, field
from datetime import datetime

from pydantic import EmailStr, TypeAdapter, ValidationError

from app.users.domain.enums import UserRole


@dataclass
class UserEntity:
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    id: int = field(default_factory=lambda: 1)
    role: UserRole = UserRole.MARKETER
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None

    def ban(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def __post_init__(self) -> None:
        try:
            TypeAdapter(EmailStr).validate_python(self.email)
        except ValidationError as e:
            raise e
