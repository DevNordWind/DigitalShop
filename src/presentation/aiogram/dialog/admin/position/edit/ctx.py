from dataclasses import dataclass
from enum import StrEnum
from typing import Final
from uuid import UUID

from domain.common.localized import Language
from domain.common.money import Currency

CTX_KEY: Final[str] = "ctx"
EDIT_POSITION_MEDIA_SCROLL: Final[str] = "EDIT_POSITION_MEDIA_SCROLL"


class MediaEditingMode(StrEnum):
    REPLACE = "REPLACE"
    ADD = "ADD"


@dataclass(slots=True)
class PositionEditingCtx:
    position_id: UUID

    current_name_lang: Language
    current_description_lang: Language
    current_currency: Currency

    media_mode: MediaEditingMode
