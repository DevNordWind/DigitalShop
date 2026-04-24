from dataclasses import dataclass
from typing import Any

from aiogram_dialog import DialogManager
from domain.common.localized import Language


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language


async def language_getter(
    dialog_manager: DialogManager,
    **_: Any,
) -> dict[str, list[LanguageButton]]:
    return {"buttons": [LanguageButton(lang=lang) for lang in Language]}
