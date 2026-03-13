import uuid
from dataclasses import dataclass, field


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
