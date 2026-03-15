import secrets
from typing import Any


class CustomID:
    def __init__(self, prefix: str = "abs_", length: int = 22) -> None:
        self.prefix = prefix
        self.length = length

    def __call__(self, *_: Any, **__: Any) -> str:
        random_part = secrets.token_urlsafe(self.length)[: self.length]
        return f"{self.prefix}{random_part}"
