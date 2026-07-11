import asyncio
import logging
from asyncio import Semaphore
from typing import Any, ClassVar, override

from aiogram.types import InlineKeyboardMarkup
from dishka import AsyncContainer
from taskiq import AsyncTaskiqDecoratedTask

from app.app.common.port.telegram_notification import (
    MessageResult,
    NotificationRequest,
    TelegramNotification,
)
from app.domain.common.localized import Language
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import TelegramContextGateway
from app.infra.common.telegram_notification.const import SEND_NOTIFICATION_TASK_NAME
from app.infra.common.telegram_notification.kb_builder import (
    NotificationKeyboardBuilder,
)
from app.infra.common.telegram_notification.text_builder import NotificationTextBuilder
from app.infra.framework.taskiq.tp import PriorityBroker

logger = logging.getLogger(__name__)

type SendNotificationTaskType = AsyncTaskiqDecoratedTask[
    [TelegramId, str, InlineKeyboardMarkup | None],
    MessageResult,
]


class TelegramNotificationImpl(TelegramNotification):
    TASK_KIQ_LIMIT: ClassVar[int] = 100

    def __init__(
        self,
        container: AsyncContainer,
        kb_builder: NotificationKeyboardBuilder,
        text_builder: NotificationTextBuilder,
        broker: PriorityBroker,
    ):
        self._container = container
        self._kb_builder = kb_builder
        self._text_builder = text_builder
        task: SendNotificationTaskType | None = broker.find_task(
            task_name=SEND_NOTIFICATION_TASK_NAME,
        )
        if not task:
            raise RuntimeError(
                f"Unregistered task: {SEND_NOTIFICATION_TASK_NAME}",
            )
        self._task = task
        self._sem: Semaphore = Semaphore(self.TASK_KIQ_LIMIT)

    @override
    async def send(
        self,
        user_id: UserId,
        request: NotificationRequest,
        **kwargs: Any,
    ) -> None:
        async with self._container() as container:
            gw: TelegramContextGateway = await container.get(
                TelegramContextGateway,
            )
            ctx: TelegramContext | None = await gw.get_by_user_id(
                user_id=user_id,
            )
            if not ctx:
                raise UserNotFoundError

        kb: dict[
            Language | None,
            InlineKeyboardMarkup,
        ] = await self._kb_builder.build(context=ctx, buttons=request.buttons)
        text: dict[Language | None, str] = await self._text_builder.build(
            context=ctx,
            key=request.key,
            **kwargs,
        )
        return await self._send(contexts=[ctx], texts=text, kbs=kb)

    @override
    async def send_admins(
        self,
        request: NotificationRequest,
        **kwargs: Any,
    ) -> None:
        async with self._container() as container:
            gw: TelegramContextGateway = await container.get(
                TelegramContextGateway,
            )
            contexts = await gw.get_admins(is_active=True)

        kb: dict[
            Language | None,
            InlineKeyboardMarkup,
        ] = await self._kb_builder.build_many(
            contexts=contexts,
            buttons=request.buttons,
        )
        text: dict[Language | None, str] = await self._text_builder.build_many(
            contexts=contexts,
            key=request.key,
            **kwargs,
        )
        return await self._send(contexts=contexts, texts=text, kbs=kb)

    async def _send(
        self,
        contexts: list[TelegramContext],
        texts: dict[Language | None, str],
        kbs: dict[Language | None, InlineKeyboardMarkup],
    ) -> None:
        async def _kiq_with_limit(ctx: TelegramContext) -> Any:
            async with self._sem:
                await self._task.kiq(
                    ctx.id,
                    texts[ctx.lang],
                    kbs.get(ctx.lang),
                )

        await asyncio.gather(*[_kiq_with_limit(ctx) for ctx in contexts])
