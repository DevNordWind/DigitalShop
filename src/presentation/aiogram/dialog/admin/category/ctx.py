from dataclasses import dataclass, field
from typing import Final
from uuid import UUID

from app.common.dto.query_params import SortingOrder
from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus

CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True, kw_only=True)
class AdminCategoryCtx:
    sorting_order: SortingOrder = field(default=SortingOrder.DESC)
    status: CategoryStatus | None = CategoryStatus.AVAILABLE

    current_category_id: UUID | None = None
    current_lang: Language
