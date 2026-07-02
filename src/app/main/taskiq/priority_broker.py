from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka

from app.config import Configuration
from app.infra.framework.sql_alchemy.table import map_all
from app.infra.framework.taskiq import (
    get_priority_broker,
)
from app.infra.framework.taskiq.tp import PriorityBroker
from app.main.ioc import PROVIDERS

CONTAINER: Final[AsyncContainer] = make_async_container(*PROVIDERS)


config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


def setup_priority_broker() -> PriorityBroker:
    map_all()
    config.log.setup_logging()
    broker = get_priority_broker(config.redis)
    setup_dishka(container=CONTAINER, broker=broker)
    return broker


priority_broker: Final[PriorityBroker] = setup_priority_broker()
