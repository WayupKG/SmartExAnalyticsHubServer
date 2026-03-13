from typing import TYPE_CHECKING, Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer

if TYPE_CHECKING:
    from collections.abc import Callable

http_bearer = HTTPBearer(auto_error=False)


x_data_token_scheme = APIKeyHeader(
    name="X-Data-Token",
    scheme_name="X-Data-Token",
    auto_error=False,
)


def verify_platform_api_token() -> Callable[
    [str | None],
    None,
]:
    def verify_x_data_token(
        token: Annotated[
            str | None,
            Security(x_data_token_scheme),
        ],
    ):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Data-Token required"
            )

    return verify_x_data_token
