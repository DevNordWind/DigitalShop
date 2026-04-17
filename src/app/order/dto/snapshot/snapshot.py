from dataclasses import dataclass
from uuid import UUID

from app.common.dto.localized import LocalizedTextDTO
from app.product.position.dto.item_content import ItemContentDTO
from app.product.position.dto.price import PositionPriceDTO


@dataclass(slots=True, frozen=True)
class ItemSnapshotDTO:
    item_id: UUID

    item_content: ItemContentDTO


@dataclass(slots=True, frozen=True)
class PositionSnapshotDTO:
    category_id: UUID
    position_id: UUID

    position_name: LocalizedTextDTO
    price: PositionPriceDTO
