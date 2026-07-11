from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.dto.file_key import FileKeyDTO
from app.app.common.dto.localized import LocalizedTextDTO
from app.app.shopping.position.dto.price import PositionPriceDTO
from app.domain.shopping.position.enums import (
    FulfillmentType,
    PositionStatus,
    WarehouseType,
)


@dataclass(slots=True, frozen=True)
class PositionDTO:
    id: UUID
    category_id: UUID
    creator_id: UUID

    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: list[FileKeyDTO]

    price: PositionPriceDTO

    fulfillment_type: FulfillmentType
    warehouse_type: WarehouseType

    created_at: datetime
    updated_at: datetime | None

    archived_at: datetime | None

    status: PositionStatus


@dataclass(slots=True, frozen=True)
class PositionWithItemsAmount:
    position: PositionDTO
    items_amount: int


@dataclass(slots=True, frozen=True)
class PositionShortDTO:
    id: UUID
    category_id: UUID
    creator_id: UUID

    name: LocalizedTextDTO
    price: PositionPriceDTO

    warehouse_type: WarehouseType
    fulfillment_type: FulfillmentType

    created_at: datetime
    archived_at: datetime | None

    status: PositionStatus


@dataclass(slots=True, frozen=True)
class PositionShortWithItemsAmount:
    position: PositionShortDTO
    items_amount: int
