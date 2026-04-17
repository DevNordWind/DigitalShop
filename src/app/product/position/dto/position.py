from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.dto.file_key import FileKeyDTO
from app.common.dto.localized import LocalizedTextDTO
from app.product.position.dto.price import PositionPriceDTO
from domain.product.position.enums import PositionStatus, WarehouseType


@dataclass(slots=True, frozen=True)
class PositionDTO:
    id: UUID
    category_id: UUID
    creator_id: UUID

    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: list[FileKeyDTO]

    price: PositionPriceDTO
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

    created_at: datetime
    archived_at: datetime | None

    status: PositionStatus
