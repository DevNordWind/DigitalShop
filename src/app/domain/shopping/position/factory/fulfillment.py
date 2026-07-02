from abc import ABC, abstractmethod

from app.domain.shopping.position.enums import FulfillmentType
from app.domain.shopping.position.strategy import FulfillmentStrategy


class FulfillmentStrategyFactory(ABC):
    @abstractmethod
    async def create(self, tp: FulfillmentType) -> FulfillmentStrategy:
        raise NotImplementedError
