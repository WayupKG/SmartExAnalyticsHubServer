from fastapi import status

from app.shared.domain.exceptions import BaseCustomException


class UserDomainError(BaseCustomException):
    """Базовый класс для всех ошибок модуля пользователей."""

    pass


class EmailAlreadyExistsError(UserDomainError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже зарегистрирован."


class UserNotFoundError(UserDomainError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден."


class InvalidCredentialsError(UserDomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль."
