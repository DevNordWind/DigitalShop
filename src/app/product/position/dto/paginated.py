from dataclasses import dataclass

from app.product.position.dto.item import ItemDTO
from app.product.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionWithItemsAmount,
)


@dataclass(slots=True, frozen=True)
class PositionsPaginated:
    positions: list[PositionDTO]
    total: int


@dataclass(slots=True, frozen=True)
class PositionWithItemsAmountPaginated:
    positions: list[PositionWithItemsAmount]
    total: int


@dataclass(slots=True, frozen=True)
class PositionsShortPaginated:
    positions: list[PositionShortDTO]
    total: int


@dataclass(slots=True, frozen=True)
class PositionItemsPaginated:
    items: list[ItemDTO]
    total: int
