from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka

from app.config import Configuration
from app.infra.framework.sql_alchemy.table import map_all
from app.infra.framework.taskiq import (
    get_broker,
)
from app.main.ioc import PROVIDERS, DishkaTaskIqActorProvider
from taskiq import AsyncBroker

CONTAINER: Final[AsyncContainer] = make_async_container(
    *(*PROVIDERS, DishkaTaskIqActorProvider())
)


config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


def setup_broker() -> AsyncBroker:
    map_all()
    config.log.setup_logging()
    broker = get_broker(config.redis)
    setup_dishka(container=CONTAINER, broker=broker)
    return broker


broker: Final[AsyncBroker] = setup_broker()
