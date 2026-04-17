from dataclasses import dataclass
from typing import Final
from uuid import UUID

from domain.common.localized import Language

CTX_KEY: Final[str] = "ctx"


@dataclass
class CategoryEditingCtx:
    category_id: UUID

    current_name_lang: Language
    current_description_lang: Language
