from __future__ import annotations

import logging
import logging.handlers
import queue
import sys
from dataclasses import dataclass
from typing import Any, override

import structlog
from asgi_correlation_id import correlation_id

__all__ = ("LoggingConfig", "shutdown_logging")


def add_correlation_id(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    request_id = correlation_id.get()
    if request_id:
        event_dict["trace_id"] = request_id
    return event_dict


_SENSITIVE_KEY_MARKERS = (
    "password",
    "passwd",
    "token",
    "secret",
    "api_key",
    "apikey",
    "authorization",
    "auth_header",
    "card_number",
    "cardnumber",
    "cvv",
    "cvc",
    "pan",
    "signature",
    "webhook_secret",
    "bot_token",
    "session_id",
    "access_token",
    "refresh_token",
    "private_key",
)


def redact_sensitive_data(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    for key, value in list(event_dict.items()):
        lowered = key.lower()
        if any(marker in lowered for marker in _SENSITIVE_KEY_MARKERS):
            event_dict[key] = _mask(value)
    return event_dict


def _mask(value: Any) -> str:
    text = str(value)
    if len(text) <= 4:  # noqa: PLR2004
        return "***"
    return f"{text[:2]}***{text[-2:]}"


class _RawQueueHandler(logging.handlers.QueueHandler):
    @override
    def prepare(self, record: logging.LogRecord) -> logging.LogRecord:
        return record


_queue_listener: logging.handlers.QueueListener | None = None


def shutdown_logging() -> None:
    global _queue_listener  # noqa: PLW0603
    if _queue_listener is not None:
        _queue_listener.stop()
        _queue_listener = None


@dataclass(slots=True, frozen=True, kw_only=True)
class LoggingConfig:
    prod: bool
    log_level: int = logging.INFO
    use_async_queue: bool = True

    def setup_logging(self) -> None:
        timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

        shared_processors: list[Any] = [
            structlog.contextvars.merge_contextvars,
            add_correlation_id,
            timestamper,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.stdlib.ExtraAdder(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),
            redact_sensitive_data,
        ]

        if self.prod:
            formatter = structlog.stdlib.ProcessorFormatter(
                foreign_pre_chain=shared_processors,
                processors=[
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.dict_tracebacks,
                    structlog.processors.JSONRenderer(),
                ],
            )
        else:
            formatter = structlog.stdlib.ProcessorFormatter(
                foreign_pre_chain=shared_processors,
                processors=[
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(colors=True),
                ],
            )

        base_handler = logging.StreamHandler(sys.stdout)
        base_handler.setFormatter(formatter)

        handler: logging.Handler
        if self.prod and self.use_async_queue:
            global _queue_listener  # noqa: PLW0603
            log_queue: queue.SimpleQueue[Any] = queue.SimpleQueue()
            handler = _RawQueueHandler(log_queue)
            _queue_listener = logging.handlers.QueueListener(
                log_queue, base_handler, respect_handler_level=True
            )
            _queue_listener.start()
        else:
            handler = base_handler

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.setLevel(self.log_level)

        for name in ("uvicorn", "uvicorn.error"):
            logging.getLogger(name).handlers.clear()
            logging.getLogger(name).propagate = True

        access_logger = logging.getLogger("uvicorn.access")
        access_logger.handlers.clear()
        access_logger.propagate = False
        access_logger.disabled = True

        for name, level in _THIRD_PARTY_LEVELS.items():
            logging.getLogger(name).setLevel(level)

        structlog.configure(
            processors=[
                *shared_processors,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(self.log_level),
            cache_logger_on_first_use=True,
        )


_THIRD_PARTY_LEVELS: dict[str, int] = {
    "sqlalchemy.engine": logging.WARNING,
    "aiogram.event": logging.WARNING,
    "aiogram.dispatcher": logging.INFO,
    "aiogram.client.session": logging.WARNING,
    "httpx": logging.WARNING,
    "httpcore": logging.WARNING,
    "asyncio": logging.WARNING,
    "apscheduler": logging.WARNING,
    "multipart": logging.WARNING,
}
