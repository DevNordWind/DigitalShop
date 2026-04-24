from dataclasses import dataclass
from typing import Final

from aiogram_dialog.api.entities import MediaAttachment
from app.common.dto.localized import LocalizedTextDTO
from domain.common.localized import Language

CTX_KEY: Final[str] = "ctx"


@dataclass(kw_only=True)
class CategoryCreationContext:
    name: LocalizedTextDTO
    description: LocalizedTextDTO
    media: MediaAttachment | None
    show_lang: Language

    name_current_lang: Language
    description_current_lang: Language
