from fastapi import status

from app.shared.presentation.schemas import ErrorDetail


class BaseCustomException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "BaseCustomException"
    detail: str = "Ошибка бизнес-логики"

    def __init__(
        self,
        error_code: str | None = None,
        detail: str | None = None,
        attr: str | None = None,
        errors: list[dict[str, str | int]] | None = None,
        status_code: int | None = None,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail
        self.error_code = error_code or self.error_code

        if errors:
            self.errors = errors
        else:
            self.errors = [
                ErrorDetail(
                    error_code=self.error_code,
                    detail=self.detail,
                    attr=attr,
                ).model_dump(),
            ]

        super().__init__(self.detail)
