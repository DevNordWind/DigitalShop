from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.localized import LocalizedTextDTO
from app.app.shopping.position.dto.item_content import ItemContentDTO
from app.app.shopping.position.dto.price import PositionPriceDTO


@dataclass(slots=True, frozen=True)
class ItemSnapshotDTO:
    id: UUID

    content: ItemContentDTO


@dataclass(slots=True, frozen=True)
class PositionSnapshotDTO:
    category_id: UUID
    position_id: UUID

    position_name: LocalizedTextDTO
    price: PositionPriceDTO
