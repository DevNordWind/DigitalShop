from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Final

from adaptix import Retort
from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from aiogram.webhook.security import IPFilter
from config import Configuration
from config.log import setup_root_logger
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from dishka.integrations.fastapi import setup_dishka as setup_fastapi
from fastapi import FastAPI
from infra.common.bootstrap import Bootstrap
from infra.framework.sql_alchemy.table import map_all
from infra.presentation.aiogram.webhook import (
    IpFilterMiddleware,
    SimpleRequestHandler,
)
from main.ioc.providers import PROVIDERS
from redis.asyncio import Redis
from taskiq import AsyncBroker

WEBHOOK_CONFIG_MISSED: Final[str] = (
    "Make sure the webhook configuration is complete!"
)
_APP_NAME: Final[str] = "bot_webhook"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    container: AsyncContainer = app.state.dishka_container
    config = await container.get(Configuration)

    if config.bot.webhook is None:
        raise RuntimeError(WEBHOOK_CONFIG_MISSED)

    bot, dp = await container.get(Bot), await container.get(Dispatcher)
    redis: Redis = await container.get(Redis)
    _ = await container.get(AsyncBroker)

    setup_dishka(container, dp)

    async with redis.lock("webhook_check"):
        webhook_info: WebhookInfo = await bot.get_webhook_info()
        if webhook_info.url != config.bot.webhook.url:
            await bot.delete_webhook(drop_pending_updates=False)
            await bot.set_webhook(
                url=config.bot.webhook.url,
                secret_token=config.bot.webhook.secret,
            )
    async with redis.lock("bootstrap_check"), container() as scope:
        bootstrap = await scope.get(Bootstrap)
        await bootstrap.check()

    yield

    await container.close()


def main() -> FastAPI:
    map_all()

    container = make_async_container(*PROVIDERS)
    raw_config = Configuration.from_yaml(retort=Retort(strict_coercion=False))
    setup_root_logger(raw_config.log, app_name=_APP_NAME)
    if raw_config.bot.webhook is None:
        raise RuntimeError(WEBHOOK_CONFIG_MISSED)

    app = FastAPI(lifespan=lifespan)
    if raw_config.bot.webhook.with_ip_filter:
        app.add_middleware(IpFilterMiddleware, ip_filter=IPFilter())  # type: ignore[arg-type]
    setup_fastapi(container, app)

    handler = SimpleRequestHandler(secret=raw_config.bot.webhook.secret)
    handler.register(app, path=raw_config.bot.webhook.path)

    return app
