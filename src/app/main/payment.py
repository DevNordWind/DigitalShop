from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_fastapi
from fastapi import FastAPI
from redis.asyncio import Redis
from taskiq import AsyncBroker

from app.config import Configuration
from app.infra.common.bootstrap import Bootstrap
from app.infra.framework.sql_alchemy.table import map_all
from app.infra.framework.taskiq.tp import PriorityBroker
from app.main.ioc import PROVIDERS
from app.presentation.fastapi import make_main_router

_APP_NAME: Final[str] = "payment_webhook"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    container: AsyncContainer = app.state.dishka_container

    redis: Redis = await container.get(Redis)
    _ = await container.get(AsyncBroker)
    __ = await container.get(PriorityBroker)

    async with redis.lock("bootstrap_check"), container() as scope:
        bootstrap = await scope.get(Bootstrap)
        await bootstrap.startup()

    yield
    await container.close()


def main() -> FastAPI:
    map_all()

    container = make_async_container(*PROVIDERS)

    app = FastAPI(lifespan=lifespan)
    app.include_router(make_main_router(app))
    setup_fastapi(container, app)

    raw_config = Configuration.from_yaml(retort=Retort(strict_coercion=False))
    raw_config.log.setup_logging()

    return app
