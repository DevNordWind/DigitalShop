from dataclasses import dataclass
from typing import Literal

from app.app.common.dto.query_params import SortingOrder


@dataclass(slots=True, frozen=True)
class CategorySortingParams:
    field: Literal["created_at"]
    order: SortingOrder
