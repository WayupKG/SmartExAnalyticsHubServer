from typing import TYPE_CHECKING, Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer
from starlette.requests import Request

from app.shared.infrastructure.unit_of_work import SQLAlchemyUnitOfWork

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Callable

    from app.shared.application.unit_of_work import IUnitOfWork


http_bearer = HTTPBearer(auto_error=False)


x_data_token_scheme = APIKeyHeader(
    name="X-Data-Token",
    scheme_name="X-Data-Token",
    auto_error=False,
)


async def get_uow(request: Request) -> AsyncGenerator[IUnitOfWork]:
    session_factory = request.app.state.db_session_factory

    uow = SQLAlchemyUnitOfWork(session_factory=session_factory)
    try:
        yield uow
    finally:
        pass


def verify_platform_api_token() -> Callable[[str | None], None]:
    def verify_x_data_token(
        token: Annotated[
            str | None,
            Security(x_data_token_scheme),
        ],
    ) -> None:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Data-Token required"
            )

    return verify_x_data_token
