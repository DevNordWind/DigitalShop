from abc import ABC, abstractmethod

from app.domain.shopping.position.enums import WarehouseType
from app.domain.shopping.position.strategy import (
    Warehouse,
)


class WarehouseFactory(ABC):
    @abstractmethod
    async def create(self, tp: WarehouseType) -> Warehouse:
        raise NotImplementedError
