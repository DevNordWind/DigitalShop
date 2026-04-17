from dataclasses import dataclass
from typing import Final
from uuid import UUID

from domain.product.position.enums import WarehouseType

CTX_KEY: Final[str] = "CTX"

CATEGORIES_SCROLL: Final[str] = "CATEGORIES_SCROLL"
CATEGORIES_HEIGHT: Final[int] = 8

POSITIONS_SCROLL: Final[str] = "POSITIONS_SCROLL"
POSITIONS_HEIGHT: Final[int] = 8

POSITION_MEDIA_SCROLL: Final[str] = "POSITIONS_MEDIA_SCROLL"


@dataclass(slots=True)
class ShoppingCtx:
    current_category_id: UUID | None
    current_position_id: UUID | None
    current_position_warehouse_type: WarehouseType | None
