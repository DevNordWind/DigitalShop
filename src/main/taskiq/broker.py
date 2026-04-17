from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import AsyncBroker

from config import Configuration
from config.log import setup_root_logger
from infra.framework.sql_alchemy.table import map_all
from infra.framework.taskiq import (
    get_broker,
)
from main.ioc import PROVIDERS

CONTAINER: Final[AsyncContainer] = make_async_container(*PROVIDERS)


config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


def setup_broker() -> AsyncBroker:
    map_all()
    setup_root_logger(config=config.log, app_name="broker")
    broker = get_broker(config.redis)
    setup_dishka(container=CONTAINER, broker=broker)
    return broker


broker: Final[AsyncBroker] = setup_broker()
