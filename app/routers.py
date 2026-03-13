__all__ = ["api_router"]

from fastapi import APIRouter

from app.users.presentation.router import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router)
