from __future__ import annotations

import time
import uuid
from typing import Any, override

import structlog
from asgi_correlation_id import correlation_id

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult

logger = structlog.get_logger("taskiq")

_TRACE_ID_LABEL = "trace_id"

_START_TIME_LABEL = "_log_start_perf_counter"


class LoggingMiddleware(TaskiqMiddleware):
    @override
    async def pre_send(self, message: TaskiqMessage) -> TaskiqMessage:
        message.labels[_TRACE_ID_LABEL] = correlation_id.get() or uuid.uuid7().hex
        return message

    @override
    async def pre_execute(self, message: TaskiqMessage) -> TaskiqMessage:
        trace_id = message.labels.get(_TRACE_ID_LABEL) or uuid.uuid4().hex
        correlation_id.set(trace_id)

        structlog.contextvars.bind_contextvars(
            trace_id=trace_id,
            task_id=message.task_id,
            task_name=message.task_name,
        )

        message.labels[_START_TIME_LABEL] = time.perf_counter()

        logger.info(
            "task_started",
            kwarg_names=list(message.kwargs.keys()) if message.kwargs else [],
        )
        return message

    @override
    async def post_execute(
        self, message: TaskiqMessage, result: TaskiqResult[Any]
    ) -> None:
        duration_ms = self._duration_ms(message)

        if result.is_err:
            logger.error(
                "task_finished_with_error",
                duration_ms=duration_ms,
                error_type=result.error.__class__.__name__ if result.error else None,
                exc_info=result.error,
            )
        else:
            logger.info("task_finished", duration_ms=duration_ms)

        self._clear_context()

    @override
    async def on_error(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
        exception: BaseException,
    ) -> None:
        logger.error(
            "task_failed",
            duration_ms=self._duration_ms(message),
            error_type=exception.__class__.__name__,
            exc_info=exception,
        )
        self._clear_context()

    @staticmethod
    def _duration_ms(message: TaskiqMessage) -> float | int:
        start = message.labels.pop(_START_TIME_LABEL, None)
        if start is None:
            return 0.0
        return round((time.perf_counter() - start) * 1000, 2)

    @staticmethod
    def _clear_context() -> None:
        structlog.contextvars.unbind_contextvars("trace_id", "task_id", "task_name")
