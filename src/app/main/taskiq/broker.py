from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from redis.asyncio import Redis
from taskiq import AsyncBroker, TaskiqEvents, TaskiqState

from app.config import Configuration
from app.infra.common.bootstrap.entities import DefaultEntitiesBootstrap
from app.infra.framework.sql_alchemy.table import map_all
from app.infra.framework.taskiq import (
    get_broker,
)
from app.main.ioc import PROVIDERS, DishkaTaskIqActorProvider

CONTAINER: Final[AsyncContainer] = make_async_container(
    *(*PROVIDERS, DishkaTaskIqActorProvider())
)


config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


async def on_startup(_: TaskiqState) -> None:
    redis: Redis = await CONTAINER.get(Redis)

    async with redis.lock("broker_bootstrap_check"), CONTAINER() as scope:
        bootstrap = await scope.get(DefaultEntitiesBootstrap)
        await bootstrap.startup()


def setup_broker() -> AsyncBroker:
    map_all()
    config.log.setup_logging()
    broker = get_broker(config.redis)
    broker.add_event_handler(event=TaskiqEvents.WORKER_STARTUP, handler=on_startup)
    setup_dishka(container=CONTAINER, broker=broker)
    return broker


broker: Final[AsyncBroker] = setup_broker()
