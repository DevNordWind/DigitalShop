from dataclasses import dataclass, field
from typing import Literal

from aiogram.enums import ContentType
from domain.common.localized import Language
from infra.authentication.telegram.model import TelegramId
from presentation.aiogram.port.broadcast.dto.button import (
    BroadcastButton,
)
from presentation.aiogram.port.broadcast.dto.const import DEFAULT_CLOSE_BUTTON
from presentation.aiogram.port.broadcast.dto.text import (
    LocalizedText,
)
from presentation.aiogram.port.broadcast.exception import (
    BroadcastTextsAsymmetrically,
)


@dataclass(slots=True, frozen=True)
class BroadcastMedia:
    type: Literal[ContentType.VIDEO, ContentType.ANIMATION, ContentType.PHOTO]
    file_id: str
    file_unique_id: str


@dataclass(slots=True, frozen=True)
class BroadcastReporting:
    report_to: TelegramId
    report_lang: Language


@dataclass(slots=True, frozen=True)
class BroadcastRequest:
    texts: LocalizedText
    reporting: BroadcastReporting
    media: BroadcastMedia | None

    buttons: tuple[BroadcastButton, ...] | None = field(
        default_factory=lambda: (DEFAULT_CLOSE_BUTTON,)
    )

    def __post_init__(self) -> None:
        if self.buttons is None:
            return

        for button in self.buttons:
            if isinstance(button.text, LocalizedText):
                for lang in button.text.texts:
                    if lang not in self.texts.texts:
                        raise BroadcastTextsAsymmetrically
