from dataclasses import dataclass
from typing import Final
from uuid import UUID

from app.app.common.dto.query_params import SortingOrder
from app.domain.shopping.position.item.enums import StockItemStatus

CTX_KEY: Final[str] = "CTX"
ITEMS_SCROLL: Final[str] = "ITEMS_SCROLL"
ITEMS_HEIGHT: Final[int] = 10


@dataclass(slots=True)
class ItemsFilters:
    order: SortingOrder
    status: StockItemStatus | None


@dataclass(slots=True, kw_only=True)
class PositionStockItemCtx:
    position_id: UUID

    current_item_id: UUID | None = None
    filters: ItemsFilters
