from dataclasses import dataclass

from app.order.dto.order import OrderDTO, PublicOrderDTO


@dataclass(slots=True, frozen=True)
class OrdersPaginated:
    orders: list[OrderDTO | PublicOrderDTO]
    total: int


@dataclass(slots=True, frozen=True)
class OrdersPaginatedByReader:
    orders: list[OrderDTO]
    total: int
