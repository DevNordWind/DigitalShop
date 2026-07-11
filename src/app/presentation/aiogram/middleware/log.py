from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any, override

import structlog
from asgi_correlation_id import correlation_id

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, Update, User

logger = structlog.get_logger("aiogram")


class LoggingContextMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        request_id = correlation_id.get() or uuid.uuid4().hex
        cid_token = correlation_id.set(request_id)
        ctx_token = structlog.contextvars.bind_contextvars(
            trace_id=request_id,
            **_extract_context(data),
        )

        start = time.perf_counter()
        status = "ok"
        try:
            return await handler(event, data)
        except Exception:
            status = "error"
            raise
        finally:
            logger.info(
                "update_processed",
                duration_ms=round((time.perf_counter() - start) * 1000, 2),
                status=status,
            )
            correlation_id.reset(cid_token)
            structlog.contextvars.reset_contextvars(**ctx_token)


def _extract_context(data: dict[str, Any]) -> dict[str, Any]:
    update: Update | None = data.get("event_update")
    user: User | None = data.get("event_from_user")
    chat: Chat | None = data.get("event_chat")

    ctx: dict[str, Any] = {}
    if update is not None:
        ctx["update_id"] = update.update_id
    if user is not None:
        ctx["user_id"] = user.id
    if chat is not None:
        ctx["chat_id"] = chat.id

    return ctx
