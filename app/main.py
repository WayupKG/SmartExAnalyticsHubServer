import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions.handlers import register_exception_handlers
from app.core.middlewares import LogCorrelationIdMiddleware
from app.core.structlog import configure as logging_configure
from app.create_app import FastAPIApp
from app.presentation import router

logging_configure()

fastapi_app = FastAPIApp()

main_app = fastapi_app.create(
    title="SmartEx Analytics Hub API",
    description="Backend server for SmartEx Analytics Hub",
)

fastapi_app.setup_custom_openapi(main_app)

main_app.add_middleware(LogCorrelationIdMiddleware)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(main_app)

main_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
