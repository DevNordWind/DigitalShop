from typing import Any, Final

from taskiq import AsyncBroker, ScheduleSource, SimpleRetryMiddleware
from taskiq.abc.serializer import TaskiqSerializer
from taskiq.serializers import ORJSONSerializer
from taskiq_redis import (
    ListRedisScheduleSource,
    RedisAsyncResultBackend,
    RedisStreamBroker,
)

from config.redis import RedisConfig
from infra.common.telegram_norification.task import (
    register_send_notification_task,
)
from infra.framework.taskiq.tp import PriorityBroker
from infra.order.task import register_auto_cancel_task
from infra.presentation.aiogram.broadcast.task import (
    register_send_msg_task,
    register_update_progress_task,
)

SERIALIZER: Final[TaskiqSerializer] = ORJSONSerializer()


def get_broker(redis_config: RedisConfig) -> AsyncBroker:
    redis_url: str = (
        f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    )

    backend: RedisAsyncResultBackend[Any] = RedisAsyncResultBackend(
        redis_url=redis_url,
        result_ex_time=10_000,
        serializer=SERIALIZER,
    )

    broker: AsyncBroker = (
        RedisStreamBroker(
            url=redis_url,
            maxlen=99_999,
        )
        .with_result_backend(backend)
        .with_middlewares(SimpleRetryMiddleware())
    )

    register_send_msg_task(broker)

    return broker


def get_priority_broker(redis_config: RedisConfig) -> PriorityBroker:
    redis_url: str = (
        f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    )

    backend: RedisAsyncResultBackend[Any] = RedisAsyncResultBackend(
        redis_url=redis_url,
        result_ex_time=10_000,
        serializer=SERIALIZER,
    )

    broker: PriorityBroker = PriorityBroker(
        RedisStreamBroker(
            url=redis_url,
            maxlen=10_000,
            queue_name="taskiq_priority",
            consumer_group_name="taskiq_priority",
        )
        .with_result_backend(backend)
        .with_middlewares(SimpleRetryMiddleware())
    )

    register_update_progress_task(broker)
    register_send_notification_task(broker)
    register_auto_cancel_task(broker)

    return broker


def get_schedule_source(redis_config: RedisConfig) -> ScheduleSource:
    redis_url: str = (
        f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    )

    return ListRedisScheduleSource(
        url=redis_url,
        serializer=SERIALIZER,
    )
