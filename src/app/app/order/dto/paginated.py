from dataclasses import dataclass

from app.app.order.dto.order import OrderDTO, PublicOrderDTO


@dataclass(slots=True, frozen=True)
class OrdersPaginated:
    orders: list[OrderDTO | PublicOrderDTO]
    total: int


@dataclass(slots=True, frozen=True)
class OrdersPaginatedByReader:
    """
    This exists because OrderReader may return only OrderDTO,
    so mapping to PublicOrderDTO happens in query handlers.
    """

    orders: list[OrderDTO]
    total: int
