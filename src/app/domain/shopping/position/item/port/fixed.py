from abc import ABC, abstractmethod

from app.domain.shopping.position.item.entity import FixedItem
from app.domain.shopping.position.item.enums import FixedItemStatus
from app.domain.shopping.position.item.value_object import (
    FixedItemId,
)
from app.domain.shopping.position.value_object import PositionId


class FixedItemRepository(ABC):
    @abstractmethod
    async def add(self, item: FixedItem) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, item_id: FixedItemId) -> FixedItem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_position_id(
        self, position_id: PositionId, status: FixedItemStatus | None = None
    ) -> list[FixedItem]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item: FixedItem) -> None:
        raise NotImplementedError
