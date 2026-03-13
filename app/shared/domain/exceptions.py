from typing import Any

from fastapi import status


class BaseCustomException(Exception):
    """
    Базовый класс для всех ошибок приложения.
    Не зависит от фреймворка.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Неизвестная ошибка бизнес-логики"

    def __init__(
        self,
        detail: str | None = None,
        error_code: str | None = None,
        attr: str | None = None,
        errors: list[dict[str, Any]] | None = None,
        status_code: int = 400,
    ) -> None:
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail

        self.error_code = error_code or self.__class__.__name__
        self.attr = attr

        if errors:
            self.errors = errors
        else:
            self.errors = [
                {
                    "error_code": self.error_code,
                    "detail": self.detail,
                    "attr": self.attr,
                }
            ]

        super().__init__(self.detail)
