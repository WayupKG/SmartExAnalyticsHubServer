from typing import TYPE_CHECKING, Any

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.shared.domain.exceptions import BaseCustomException
from app.shared.presentation.schemas import ErrorDetail

if TYPE_CHECKING:
    from collections.abc import Callable

    from gunicorn.glogging import Logger

logger: Logger = structlog.get_logger("uvicorn.error")


def handle_request_validation_error(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors": [
                ErrorDetail(
                    error_code=error.get("type", "validation_error"),
                    detail=error.get("msg"),
                    attr=".".join(map(str, error.get("loc", [])))
                    if error.get("loc")
                    else "body",
                ).model_dump()
                for error in exc.errors()
            ],
        },
    )


def handle_custom_exception(
    _request: Request,
    exc: BaseCustomException,
) -> JSONResponse:
    """Универсальный обработчик для всех кастомных ошибок."""

    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(f"Server Error ({exc.status_code}): {exc.detail}", exc_info=True)
    else:
        logger.warning(f"Client Error ({exc.status_code}): {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            # Оборачиваем сырые словари в Pydantic только перед отправкой
            "errors": [ErrorDetail(**err).model_dump() for err in exc.errors],
        },
    )


def handle_unexpected_exception(
    _request: Request,
    _exc: Exception,
) -> JSONResponse:
    logger.exception("Unhandled Internal Server Error occurred")
    detail = (
        ", ".join(map(str, _exc.args)) if _exc.args else "Внутренняя ошибка сервера"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "errors": [
                ErrorDetail(
                    error_code=_exc.__class__.__name__,
                    detail=detail,
                    attr=None,
                ).model_dump()
            ],
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    exception_handlers: dict[
        type[Exception], Callable[[Request, Any], JSONResponse]
    ] = {
        RequestValidationError: handle_request_validation_error,
        BaseCustomException: handle_custom_exception,
        Exception: handle_unexpected_exception,
    }

    for exc, handler in exception_handlers.items():
        app.add_exception_handler(exc, handler)
