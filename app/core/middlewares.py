from typing import TYPE_CHECKING

import structlog

from app.core.structlog import generate_correlation_id

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class LogCorrelationIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        structlog.contextvars.bind_contextvars(
            correlation_id=generate_correlation_id(),
            method=scope["method"],
            path=scope["path"],
        )

        try:
            await self.app(scope, receive, send)
        finally:
            structlog.contextvars.unbind_contextvars(
                "correlation_id",
                "method",
                "path",
            )
        return None
