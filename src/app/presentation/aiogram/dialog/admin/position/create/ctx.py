from dataclasses import dataclass
from typing import Final
from uuid import UUID

from aiogram_dialog.api.entities import MediaAttachment

from app.app.common.dto.localized import LocalizedTextDTO
from app.app.shopping.position.dto.price import PositionPriceDTO
from app.domain.common.localized import Language
from app.domain.common.money import Currency
from app.domain.shopping.position.enums import WarehouseType

CTX_KEY: Final[str] = "ctx"

MEDIA_SCROLL: Final[str] = "MEDIA_SCROLL"


@dataclass(kw_only=True)
class PositionCreationCtx:
    category_id: UUID

    name: LocalizedTextDTO
    description: LocalizedTextDTO
    media: list[MediaAttachment]
    price: PositionPriceDTO

    show_lang: Language
    warehouse_type: WarehouseType | None

    name_current_lang: Language
    description_current_lang: Language
    current_currency: Currency

    @property
    def can_confirm(self) -> bool:
        return (
            len(self.price.prices) == len(Currency)
            and bool(self.name.translations)
            and self.warehouse_type is not None
        )
