from dataclasses import dataclass
from typing import Final
from uuid import UUID

from app.app.common.dto.query_params import SortingOrder
from app.domain.common.localized import Language
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.position.enums import PositionStatus

CATEGORIES_SCROLL: Final[str] = "CATEGORIES_SCROLL"
CATEGORIES_PAGE_LIMIT: Final[int] = 8

POSITIONS_SCROLL: Final[str] = "POSITIONS_SCROLL"
POSITIONS_PAGE_LIMIT: Final[int] = 8

POSITION_MEDIA_SCROLL: Final[str] = "POSITION_MEDIA_SCROLL"


CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True, kw_only=True)
class AdminPositionCtx:
    category_sorting_order: SortingOrder = SortingOrder.DESC
    category_status: CategoryStatus | None = CategoryStatus.AVAILABLE

    position_sorting_order: SortingOrder = SortingOrder.DESC
    position_status: PositionStatus | None = PositionStatus.AVAILABLE

    current_category_id: UUID | None = None
    current_position_id: UUID | None = None

    current_lang: Language
