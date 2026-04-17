from dataclasses import dataclass
from typing import Literal

from app.common.dto.query_params import SortingOrder


@dataclass(slots=True, frozen=True)
class PositionSortingParams:
    field: Literal["created_at"]
    order: SortingOrder


@dataclass(slots=True, frozen=True)
class PositionItemsSortingParams:
    field: Literal["created_at", "archived_at"]
    order: SortingOrder
