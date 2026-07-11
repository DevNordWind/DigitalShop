from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.dto.file_key import FileKeyDTO
from app.app.common.dto.localized import LocalizedTextDTO
from app.domain.shopping.category.enums import CategoryStatus


@dataclass(slots=True, frozen=True)
class CategoryDTO:
    id: UUID
    creator_id: UUID

    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: FileKeyDTO | None

    created_at: datetime
    updated_at: datetime | None
    archived_at: datetime | None

    status: CategoryStatus


@dataclass(slots=True, frozen=True)
class CategoryShortDTO:
    id: UUID
    name: LocalizedTextDTO

    created_at: datetime
    archived_at: datetime | None

    status: CategoryStatus


@dataclass(slots=True, frozen=True)
class CategoryWithGoodsAmountDTO:
    category: CategoryDTO
    positions_amount: int
    items_amount: int
