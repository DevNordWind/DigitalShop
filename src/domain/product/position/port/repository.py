from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.enums import PositionStatus
from domain.product.position.item.entity import FiniteItem, Item
from domain.product.position.item.enums import (
    ItemStatus,
)
from domain.product.position.item.value_object import ItemId
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.product.position.value_object import PositionId


class PositionRepository(ABC):
    @abstractmethod
    async def add(self, position: Position) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, item: Item) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_items(self, items: Sequence[Item]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        position_id: PositionId,
    ) -> Position | None:
        raise NotImplementedError

    @abstractmethod
    async def get_for_update(self, position_id: PositionId) -> Position | None:
        raise NotImplementedError

    @abstractmethod
    async def get_items_for_update(
        self,
        position_id: PositionId,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    async def get_finite_items_by_ids(
        self,
        items_ids: Sequence[ItemId],
    ) -> list[FiniteItem]:
        raise NotImplementedError

    @abstractmethod
    async def get_items_for_update_by_category_ids(
        self,
        category_ids: Sequence[CategoryId],
        status: ItemStatus | None = None,
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    async def get_item_for_update(self, item_id: ItemId) -> Item | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_category_ids_for_update(
        self,
        category_ids: Sequence[CategoryId],
        status: PositionStatus | None = None,
    ) -> list[Position]:
        raise NotImplementedError

    @abstractmethod
    async def acquire_items_for_update(
        self,
        position_id: PositionId,
        amount: ItemsAmount,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    async def acquire_items(
        self,
        position_id: PositionId,
        amount: ItemsAmount,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    async def get_item_category_id(self, item_id: ItemId) -> CategoryId | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, position: Position) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, item: Item) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_items(
        self,
        position_id: PositionId,
        status: ItemStatus | None = ItemStatus.AVAILABLE,
    ) -> int:
        raise NotImplementedError
