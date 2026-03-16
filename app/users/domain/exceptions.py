from app.shared.domain.exceptions import BaseCustomException


class EmailAlreadyExistsError(BaseCustomException):
    status_code = 409
    error_code = "EmailAlreadyExistsError"
    detail = "Пользователь с таким email уже зарегистрирован."


class UserNotFoundError(BaseCustomException):
    status_code = 404
    error_code = "UserNotFoundError"
    detail = "Пользователь не найден."


class InvalidCredentialsError(BaseCustomException):
    status_code = 401
    error_code = "InvalidCredentialsError"
    detail = "Неверный email или пароль."
