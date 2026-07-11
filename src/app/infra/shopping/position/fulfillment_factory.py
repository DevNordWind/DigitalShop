from typing import override

from dishka import AsyncContainer
from frozendict import frozendict

from app.domain.shopping.position.enums import FulfillmentType
from app.domain.shopping.position.factory import (
    FulfillmentStrategyFactory,
)
from app.domain.shopping.position.strategy import (
    FixedFulfillment,
    FulfillmentStrategy,
    StockFulfillment,
)


class DishkaFulfillmentStrategyFactory(FulfillmentStrategyFactory):
    MAPPING: frozendict[FulfillmentType, type[FulfillmentStrategy]] = frozendict(
        {
            FulfillmentType.FIXED: FixedFulfillment,
            FulfillmentType.STOCK: StockFulfillment,
        }
    )

    def __init__(self, container: AsyncContainer):
        self._container = container

    @override
    async def create(self, tp: FulfillmentType) -> FulfillmentStrategy:
        return await self._container.get(self.MAPPING[tp])
