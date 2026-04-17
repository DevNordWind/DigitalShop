from dataclasses import dataclass
from typing import Final

from domain.common.localized import Language
from presentation.aiogram.port.broadcast import BroadcastMedia
from presentation.aiogram.port.broadcast.dto import UrlButton

CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True, kw_only=True)
class BroadcastSetup:
    media: BroadcastMedia | None = None
    texts: dict[Language, str]
    url_buttons: list[UrlButton]

    with_close_button: bool = True


@dataclass(slots=True)
class BroadcastCtx:
    current_preview_lang: Language | None
    current_texts_lang: Language

    setup: BroadcastSetup

    @property
    def can_start(self) -> bool:
        return bool(self.setup.texts)
