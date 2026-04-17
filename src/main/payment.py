from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_fastapi
from fastapi import FastAPI
from redis.asyncio import Redis
from taskiq import AsyncBroker

from config import Configuration
from config.log import setup_root_logger
from infra.common.bootstrap import Bootstrap
from infra.framework.sql_alchemy.table import map_all
from main.ioc.providers import PROVIDERS
from presentation.http.webhook.payment import payments_router

_APP_NAME: Final[str] = "payment_webhook"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    container: AsyncContainer = app.state.dishka_container

    redis: Redis = await container.get(Redis)
    _ = await container.get(AsyncBroker)

    async with redis.lock("bootstrap_check"), container() as scope:
        bootstrap = await scope.get(Bootstrap)
        await bootstrap.check()

    yield


def main() -> FastAPI:
    map_all()

    container = make_async_container(*PROVIDERS)

    app = FastAPI(lifespan=lifespan)
    app.include_router(router=payments_router)
    setup_fastapi(container, app)

    raw_config = Configuration.from_yaml(retort=Retort(strict_coercion=False))
    setup_root_logger(raw_config.log, app_name=_APP_NAME)

    return app
