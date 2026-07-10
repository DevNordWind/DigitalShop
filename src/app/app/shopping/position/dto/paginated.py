from dataclasses import dataclass

from app.app.shopping.position.dto.item import ItemDTO
from app.app.shopping.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionShortWithItemsAmount,
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
class PositionShortWithItemsAmountPaginated:
    positions: list[PositionShortWithItemsAmount]
    total: int


@dataclass(slots=True, frozen=True)
class PositionsShortPaginated:
    positions: list[PositionShortDTO]
    total: int


@dataclass(slots=True, frozen=True)
class PositionItemsPaginated:
    items: list[ItemDTO]
    total: int
