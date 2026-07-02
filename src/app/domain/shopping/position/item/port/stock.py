from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.domain.shopping.position.item.entity import StockItem
from app.domain.shopping.position.item.enums import StockItemStatus
from app.domain.shopping.position.item.value_object import ItemsAmount, StockItemId
from app.domain.shopping.position.value_object import PositionId


class StockItemRepository(ABC):
    @abstractmethod
    async def add_many(self, items: Sequence[StockItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, item_id: StockItemId) -> StockItem | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire_by_position_id(
        self,
        position_id: PositionId,
        amount: ItemsAmount | None = None,
        status: StockItemStatus | None = None,
    ) -> list[StockItem]:
        raise NotImplementedError

    @abstractmethod
    async def acquire_by_ids(
        self,
        ids: Sequence[StockItemId],
    ) -> list[StockItem]:
        raise NotImplementedError

    @abstractmethod
    async def count_items(
        self,
        position_id: PositionId,
        status: StockItemStatus | None = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item: StockItem) -> None:
        raise NotImplementedError
