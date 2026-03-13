from fastapi import APIRouter

from app.presentation.rest import router as router_api

router = APIRouter()

router.include_router(router=router_api)
