from dataclasses import dataclass
from typing import Final
from uuid import UUID

from app.common.dto.query_params import SortingOrder
from domain.order.enums import OrderStatus

ORDER_SCROLL: Final[str] = "ORDER_SCROLL"
ORDER_HEIGHT: Final[int] = 8

CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True)
class OrdersFilters:
    sorting_order: SortingOrder
    status: OrderStatus | None = None


@dataclass(slots=True)
class OrdersCtx:
    current_user_id: UUID

    filters: OrdersFilters

    current_order_id: UUID | None = None
