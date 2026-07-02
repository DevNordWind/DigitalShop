from fastapi import APIRouter

from app.presentation.fastapi.health.schema import OK_RESPONSE, OkResponse

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/")
async def health() -> OkResponse:
    return OK_RESPONSE
