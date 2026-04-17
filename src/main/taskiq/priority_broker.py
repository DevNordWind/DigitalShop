from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka

from config import Configuration
from config.log import setup_root_logger
from infra.framework.sql_alchemy.table import map_all
from infra.framework.taskiq import (
    get_priority_broker,
)
from infra.framework.taskiq.tp import PriorityBroker
from main.ioc import PROVIDERS

CONTAINER: Final[AsyncContainer] = make_async_container(*PROVIDERS)


config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


def setup_priority_broker() -> PriorityBroker:
    map_all()
    setup_root_logger(config=config.log, app_name="priority_broker")
    broker = get_priority_broker(config.redis)
    setup_dishka(container=CONTAINER, broker=broker)
    return PriorityBroker(broker)


priority_broker: Final[PriorityBroker] = setup_priority_broker()
