from dataclasses import dataclass, field
from typing import Final

from domain.common.localized import Language

CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True, kw_only=True)
class UrlButtonCtx:
    names: dict[Language, str] = field(default_factory=dict)
    url: str | None = None

    show_on: Language
    current_name_lang: Language

    @property
    def can_create(self) -> bool:
        return bool(self.names) and self.url is not None
