from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

import structlog
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.core.database import db_helper

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from app.core.structlog import Logger

logger: Logger = structlog.get_logger(__name__)


class FastAPIApp:
    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
        app.state.db_session_factory = db_helper.session_factory
        yield
        await db_helper.dispose()

    def create(
        self,
        title: str,
        description: str,
        custom_docs_url: str | None = None,
    ) -> FastAPI:
        app = FastAPI(
            title=title,
            description=description,
            lifespan=self.lifespan,
            docs_url=custom_docs_url if custom_docs_url else "/docs",
            redoc_url=None,
            version="0.1.0",
            openapi_url="/api/v1/openapi.json",
        )

        self.setup_custom_openapi(app)
        return app

    @staticmethod
    def setup_custom_openapi(app: FastAPI) -> None:
        def custom_openapi() -> dict[str, Any]:
            if app.openapi_schema:
                return app.openapi_schema

            schema = get_openapi(
                title=app.title,
                version=app.version,
                routes=app.routes,
            )

            components = schema.setdefault("components", {})
            schemas = components.setdefault("schemas", {})

            schemas["ErrorDetail"] = {
                "type": "object",
                "properties": {
                    "error_code": {"type": "string", "nullable": True},
                    "detail": {"type": "string", "nullable": True},
                    "attr": {"type": "string", "nullable": True},
                },
            }

            schemas["ErrorResponse"] = {
                "type": "object",
                "properties": {
                    "errors": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ErrorDetail"},
                    },
                },
                "required": ["errors"],  # Убрали обязательность exception_type
            }

            error_response_ref = {"$ref": "#/components/schemas/ErrorResponse"}

            for path_item in schema.get("paths", {}).values():
                for operation in path_item.values():
                    if not isinstance(operation, dict):
                        continue
                    responses = operation.setdefault("responses", {})

                    # Очищаем стандартные 422, чтобы не путать фронтенд
                    responses.pop("422", None)

                    for code in ["400", "422", "500"]:
                        responses.setdefault(
                            code,
                            {
                                "description": "Error Response",
                                "content": {
                                    "application/json": {"schema": error_response_ref}
                                },
                            },
                        )

            app.openapi_schema = schema
            return app.openapi_schema

        app.openapi = custom_openapi  # type: ignore[method-assign]
