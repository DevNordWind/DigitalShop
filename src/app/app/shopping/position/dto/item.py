from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.shopping.position.dto.item_content import ItemContentDTO
from app.domain.shopping.position.item.enums import (
    FixedItemStatus,
    GenericItemStatus,
    StockItemStatus,
)


@dataclass(slots=True, frozen=True)
class FixedItemDTO:
    id: UUID
    position_id: UUID
    creator_id: UUID

    content: ItemContentDTO
    status: FixedItemStatus

    created_at: datetime

    archived_at: datetime | None
    updated_at: datetime | None


@dataclass(slots=True, frozen=True)
class StockItemDTO:
    id: UUID
    position_id: UUID
    creator_id: UUID

    content: ItemContentDTO
    status: StockItemStatus

    created_at: datetime

    archived_at: datetime | None
    sold_at: datetime | None
    reserved_at: datetime | None
    updated_at: datetime | None


type ItemDTO = StockItemDTO | FixedItemDTO
type ItemStatus = GenericItemStatus | FixedItemStatus | StockItemStatus
