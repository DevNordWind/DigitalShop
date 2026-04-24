from typing import Any, Final

from config.redis import RedisConfig
from infra.common.telegram_notification.task import (
    register_send_notification_task,
)
from infra.framework.taskiq.tp import PriorityBroker
from infra.order.task import register_auto_cancel_task
from infra.presentation.aiogram.broadcast.task import (
    register_send_msg_task,
    register_update_progress_task,
)
from taskiq import AsyncBroker, ScheduleSource, SimpleRetryMiddleware
from taskiq.abc.serializer import TaskiqSerializer
from taskiq.serializers import ORJSONSerializer
from taskiq_redis import (
    ListRedisScheduleSource,
    RedisAsyncResultBackend,
    RedisStreamBroker,
)

SERIALIZER: Final[TaskiqSerializer] = ORJSONSerializer()


def get_broker(redis_config: RedisConfig) -> AsyncBroker:
    backend: RedisAsyncResultBackend[Any] = RedisAsyncResultBackend(
        redis_url=redis_config.url,
        result_ex_time=10_000,
        serializer=SERIALIZER,
    )

    broker: AsyncBroker = (
        RedisStreamBroker(
            url=redis_config.url,
            maxlen=99_999,
        )
        .with_result_backend(backend)
        .with_middlewares(SimpleRetryMiddleware())
    )

    register_send_msg_task(broker)

    return broker


def get_priority_broker(redis_config: RedisConfig) -> PriorityBroker:
    backend: RedisAsyncResultBackend[Any] = RedisAsyncResultBackend(
        redis_url=redis_config.url,
        result_ex_time=10_000,
        serializer=SERIALIZER,
    )

    broker: PriorityBroker = PriorityBroker(
        RedisStreamBroker(
            url=redis_config.url,
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
    return ListRedisScheduleSource(
        url=redis_config.url,
        serializer=SERIALIZER,
    )
