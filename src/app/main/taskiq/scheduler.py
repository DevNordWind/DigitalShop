from typing import Final

from adaptix import Retort
from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import ScheduleSource, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from app.config import Configuration
from app.infra.framework.sql_alchemy.table import map_all
from app.infra.framework.taskiq import (
    get_priority_broker,
    get_schedule_source,
)
from app.infra.framework.taskiq.tp import PriorityBroker
from app.main.ioc import PROVIDERS, DishkaTaskIqActorProvider

CONTAINER: Final[AsyncContainer] = make_async_container(
    *(*PROVIDERS, DishkaTaskIqActorProvider())
)

config: Final[Configuration] = Configuration.from_yaml(
    retort=Retort(strict_coercion=False),
)


def setup_priority_broker() -> PriorityBroker:
    map_all()
    broker = get_priority_broker(config.redis)
    setup_dishka(container=CONTAINER, broker=broker)

    return broker


def setup_scheduler() -> ScheduleSource:
    config.log.setup_logging()
    return get_schedule_source(redis_config=config.redis)


priority_broker: Final[PriorityBroker] = setup_priority_broker()

source: Final[ScheduleSource] = setup_scheduler()

scheduler: Final[TaskiqScheduler] = TaskiqScheduler(
    broker=priority_broker,
    sources=[
        source,
        LabelScheduleSource(priority_broker),
    ],
)
