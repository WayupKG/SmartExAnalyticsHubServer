import uuid
from dataclasses import dataclass, field

from pydantic import EmailStr, TypeAdapter, ValidationError


@dataclass
class User:
    email: str
    hashed_password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True

    def ban(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def __post_init__(self) -> None:
        try:
            TypeAdapter(EmailStr).validate_python(self.email)
        except ValidationError as e:
            raise e
