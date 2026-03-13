__all__ = ["router"]


from fastapi import APIRouter, Depends

from app.core.config import settings
from app.presentation.rest.dependencies.base import http_bearer

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[
        Depends(http_bearer),
    ],
)
