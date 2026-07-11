from dataclasses import dataclass
from typing import Any

import structlog
from aiogram.types import CallbackQuery, Message

from app.app.common.exception import AppError
from app.domain.common.coefficient import (
    CoefficientTooBigError,
    CoefficientTooSmallError,
)
from app.domain.common.exception import DomainError
from app.domain.wallet.exception import InsufficientFundsError
from app.presentation.aiogram.port import Text
from app.presentation.aiogram.util.error_translator.formatter import (
    CoefficientErrorExtractor,
    ErrorContextExtractor,
    InsufficientFundsErrorExtractor,
)

logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class ErrorTranslatorConfig:
    message_fallback_key: str = "fallback-error"
    callback_fallback_key: str = "fallback-error.call"
    message_unexpected_fallback_key: str = "unexpected-error"
    callback_unexpected_fallback_key: str = "unexpected-error.call"

    def get_fallback_by_event_type(self, event: Message | CallbackQuery) -> str:
        match event:
            case Message():
                return self.message_fallback_key
            case CallbackQuery():
                return self.callback_fallback_key

    def get_unexpected_fallback_by_event_type(
        self, event: Message | CallbackQuery
    ) -> str:
        match event:
            case Message():
                return self.message_unexpected_fallback_key
            case CallbackQuery():
                return self.callback_unexpected_fallback_key


class ErrorTranslator:
    def __init__(self, text: Text, config: ErrorTranslatorConfig):
        self.config = config
        self._text = text
        self._extractors: dict[type[Exception], ErrorContextExtractor] = {
            CoefficientTooSmallError: CoefficientErrorExtractor(),
            CoefficientTooBigError: CoefficientErrorExtractor(),
            InsufficientFundsError: InsufficientFundsErrorExtractor(),
        }

    def register_extractor(
        self, exc_type: type[Exception], extractor: ErrorContextExtractor
    ) -> None:
        self._extractors[exc_type] = extractor

    def translate_error(
        self, exc: DomainError | AppError, event: CallbackQuery | Message
    ) -> str:
        exc_vars: dict[str, Any] = self._extract_ctx(exc)
        resolved_key: str = self._resolve_key(exc=exc, event=event)

        return self._text(resolved_key, **exc_vars)

    def translate_unexpected_error(self, event: CallbackQuery | Message) -> str:
        return self._text(
            key=self.config.get_unexpected_fallback_by_event_type(event=event)
        )

    def _extract_ctx(self, exc: Exception) -> dict[str, Any]:
        extractor = self._extractors.get(type(exc))
        if extractor:
            return extractor.extract(exc)

        return vars(exc)

    def _resolve_key(
        self, exc: DomainError | AppError, event: Message | CallbackQuery
    ) -> str:
        exc_name: str = exc.__class__.__name__

        if not self._text.key_exists(key=exc_name):
            logger.warning(
                "error_translation_missing", error_type=exc.__class__.__name__
            )
            for tp in type(exc).__mro__:
                if self._text.key_exists(key=tp.__name__):
                    return self._format_key(key=tp.__name__, event=event)

            return self.config.get_fallback_by_event_type(event=event)

        return self._format_key(key=exc_name, event=event)

    def _format_key(self, key: str, event: CallbackQuery | Message) -> str:
        if isinstance(event, CallbackQuery):
            return f"{key}.call"

        return key
