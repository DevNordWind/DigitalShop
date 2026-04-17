import asyncio
import logging
from typing import ClassVar
from uuid import UUID

from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup
from dishka import AsyncContainer
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask

from domain.common.localized import Language
from domain.common.port import UUIDProvider
from infra.authentication.telegram.model import TelegramContext
from infra.authentication.telegram.port import TelegramContextGateway
from infra.framework.taskiq.tp import PriorityBroker
from presentation.aiogram.port.broadcast import (
    BroadcastMedia,
    BroadcastRequest,
    TelegramBroadcaster,
)
from presentation.aiogram.port.broadcast.dto import BroadcastReporting

from .const import SEND_MSG_TASK_NAME, UPDATE_PROGRESS_TASK_NAME
from .dto import BroadcastProgress, MessageResult
from .kb_builder import BroadcastKeyboardBuilder
from .progress import BroadcastProgressGateway, BroadcastProgressMessage

type SendMsgTaskType = AsyncTaskiqDecoratedTask[
    [UUID, int, str, InlineKeyboardMarkup | None, BroadcastMedia | None],
    MessageResult,
]
type UpdateProgressTaskType = AsyncTaskiqDecoratedTask[
    [UUID, BroadcastReporting], None
]

logger = logging.getLogger(__name__)


class TelegramBroadcasterImpl(TelegramBroadcaster):
    CHUNK_SIZE: ClassVar[int] = 150

    def __init__(
        self,
        broker: AsyncBroker,
        priority_broker: PriorityBroker,
        kb_builder: BroadcastKeyboardBuilder,
        progress_gw: BroadcastProgressGateway,
        progress_msg: BroadcastProgressMessage,
        container: AsyncContainer,
        uuid_provider: UUIDProvider,
    ):
        msg_task = broker.find_task(task_name=SEND_MSG_TASK_NAME)
        if msg_task is None:
            raise RuntimeError(f"Task: {SEND_MSG_TASK_NAME} not found")

        update_task = priority_broker.find_task(
            task_name=UPDATE_PROGRESS_TASK_NAME
        )
        if update_task is None:
            raise RuntimeError(f"Task: {UPDATE_PROGRESS_TASK_NAME} not found")

        self._msg_task: SendMsgTaskType = msg_task
        self._update_task: UpdateProgressTaskType = update_task
        self._kb_builder: BroadcastKeyboardBuilder = kb_builder
        self._progress_gw: BroadcastProgressGateway = progress_gw
        self._progress_msg: BroadcastProgressMessage = progress_msg
        self._uuid: UUIDProvider = uuid_provider
        self._container: AsyncContainer = container

    async def broadcast(self, request: BroadcastRequest) -> None:
        async with self._container() as container:
            gateway: TelegramContextGateway = await container.get(
                TelegramContextGateway
            )
            contexts: list[TelegramContext] = await gateway.get_all_by_langs(
                is_active=True, langs=list(request.texts.texts.keys())
            )
        langs: set[Language] = {
            ctx.lang for ctx in contexts if ctx.lang is not None
        }
        markups: dict[Language, InlineKeyboardMarkup] | None = None
        if request.buttons:
            markups = self._kb_builder.build_many(
                langs=langs, buttons=request.buttons
            )

        await self._broadcast(request, contexts, markups)

    async def _broadcast(
        self,
        request: BroadcastRequest,
        contexts: list[TelegramContext],
        markups: dict[Language, InlineKeyboardMarkup] | None,
    ) -> None:
        progress: BroadcastProgress = await self._start_progress(
            request=request, total=len(contexts)
        )
        await self._progress_gw.set(progress)

        for i in range(0, len(contexts), self.CHUNK_SIZE):
            chunk = contexts[i : i + self.CHUNK_SIZE]
            await asyncio.gather(
                *[
                    self._msg_task.kiq(
                        progress.id,
                        ctx.id,
                        request.texts.texts[ctx.lang],  # type: ignore[index]
                        markups[ctx.lang] if markups is not None else None,  # type: ignore[index]
                        request.media,
                    )
                    for ctx in chunk
                ]
            )
            await asyncio.sleep(0)

        if progress.current_message_id:
            await self._update_task.kiq(progress.id, request.reporting)

    async def _start_progress(
        self, request: BroadcastRequest, total: int
    ) -> BroadcastProgress:
        start_msg_id: int | None = None

        try:
            start_msg_id = (
                await self._progress_msg.start(
                    reporting=request.reporting, total=total
                )
            ).message_id
        except TelegramAPIError as e:
            logger.error(f"Failed to send start message: {e}")

        broadcast_id: UUID = self._uuid()

        return BroadcastProgress(
            id=broadcast_id,
            success=0,
            error=0,
            not_active=0,
            total=total,
            current_message_id=start_msg_id,
        )
