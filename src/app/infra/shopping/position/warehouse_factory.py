from typing import override

from dishka import AsyncContainer
from frozendict import frozendict

from app.domain.shopping.position.enums import WarehouseType
from app.domain.shopping.position.factory import WarehouseFactory
from app.domain.shopping.position.strategy import (
    FixedWarehouse,
    UnlimitedWarehouse,
    Warehouse,
)


class DishkaWarehouseFactory(WarehouseFactory):
    MAPPING: frozendict[WarehouseType, type[Warehouse]] = frozendict(
        {
            WarehouseType.FIXED: FixedWarehouse,
            WarehouseType.UNLIMITED: UnlimitedWarehouse,
        }
    )

    def __init__(self, container: AsyncContainer):
        self._container = container

    @override
    async def create(self, tp: WarehouseType) -> Warehouse:
        return await self._container.get(self.MAPPING[tp])
