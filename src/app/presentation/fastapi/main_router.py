from fastapi import APIRouter, FastAPI

from app.presentation.fastapi.health import health_router
from app.presentation.fastapi.webhook import payments_router

main_router = APIRouter(prefix="/api/v1")


def make_main_router(app: FastAPI) -> APIRouter:
    main_router.include_router(payments_router)
    main_router.include_router(health_router)

    return main_router
