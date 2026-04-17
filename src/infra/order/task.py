import logging
from datetime import timedelta
from typing import Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.order.cmd import ExpireOutdatedOrders
from infra.framework.taskiq.tp import PriorityBroker

logger = logging.getLogger(__name__)
AUTO_CANCEL_TASK_NAME: Final[str] = "AUTO_CANCEL_TASK"


def register_auto_cancel_task(
    broker: PriorityBroker,
) -> None:
    broker.register_task(
        func=auto_cancel_task,
        task_name=AUTO_CANCEL_TASK_NAME,
        schedule=[{"interval": timedelta(seconds=30)}],
    )


@inject(patch_module=True)
async def auto_cancel_task(handler: FromDishka[ExpireOutdatedOrders]) -> None:
    await handler()
