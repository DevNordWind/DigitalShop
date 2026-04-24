from abc import ABC, abstractmethod
from datetime import datetime

from domain.product.position.enums.warehouse import WarehouseType
from domain.product.position.exception.position import (
    PositionWarehouseFull,
)
from domain.product.position.item.entity import FiniteItem


class WarehouseStrategy(ABC):
    @property
    @abstractmethod
    def type(self) -> WarehouseType:
        raise NotImplementedError

    @abstractmethod
    def ensure_can_add(self, current: int, to_add: int) -> None:
        raise NotImplementedError


class FiniteWarehouse(WarehouseStrategy, ABC):
    @abstractmethod
    def acquire(self, item: FiniteItem, now: datetime) -> FiniteItem:
        raise NotImplementedError


class InfiniteWarehouse(WarehouseStrategy, ABC): ...


class FixedWarehouse(InfiniteWarehouse):
    @property
    def type(self) -> WarehouseType:
        return WarehouseType.FIXED

    def ensure_can_add(self, current: int, to_add: int) -> None:
        if current + to_add > 1:
            raise PositionWarehouseFull


class StockWarehouse(FiniteWarehouse):
    @property
    def type(self) -> WarehouseType:
        return WarehouseType.STOCK

    def ensure_can_add(self, current: int, to_add: int) -> None:
        """There is not any limitation"""

    def acquire(self, item: FiniteItem, now: datetime) -> FiniteItem:
        item.reserve(now)
        return item
