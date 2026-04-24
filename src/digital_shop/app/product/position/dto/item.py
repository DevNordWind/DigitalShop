from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.product.position.dto.item_content import ItemContentDTO
from domain.product.position.item.enums import ItemStatus


@dataclass(slots=True, frozen=True)
class FiniteItemDTO:
    id: UUID
    position_id: UUID
    creator_id: UUID

    content: ItemContentDTO
    status: ItemStatus

    archived_at: datetime | None
    sold_at: datetime | None
    reserved_at: datetime | None

    created_at: datetime
    updated_at: datetime | None


@dataclass(slots=True, frozen=True)
class InfiniteItemDTO:
    id: UUID
    position_id: UUID
    creator_id: UUID

    content: ItemContentDTO
    status: ItemStatus
    archived_at: datetime | None

    created_at: datetime
    updated_at: datetime | None


type ItemDTO = InfiniteItemDTO | FiniteItemDTO
