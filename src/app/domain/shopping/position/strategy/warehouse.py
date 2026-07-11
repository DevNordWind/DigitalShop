from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from typing import override
from uuid import UUID

from app.domain.shopping.position.exception import (
    NothingToAddError,
    OutOfStockError,
    PositionWarehouseFullError,
)
from app.domain.shopping.position.item.entity import FixedItem, StockItem
from app.domain.shopping.position.item.enums import FixedItemStatus, StockItemStatus
from app.domain.shopping.position.item.exception import (
    FixedItemNotFoundError,
    StockItemNotFoundError,
)
from app.domain.shopping.position.item.factory import FixedItemFactory, StockItemFactory
from app.domain.shopping.position.item.port import (
    FixedItemRepository,
    StockItemRepository,
)
from app.domain.shopping.position.item.value_object import (
    FixedItemId,
    ItemContent,
    ItemsAmount,
    ItemSnapshot,
    StockItemId,
)
from app.domain.shopping.position.value_object import PositionId
from app.domain.user.value_object import UserId


class Warehouse(ABC):
    async def add(
        self,
        creator_id: UserId,
        position_id: PositionId,
        contents: Sequence[ItemContent],
    ) -> tuple[ItemSnapshot, ...]:
        if not contents:
            raise NothingToAddError

        return await self._add(
            creator_id=creator_id, position_id=position_id, contents=contents
        )

    @abstractmethod
    async def replace(
        self, item_id: UUID, new_content: ItemContent, now: datetime
    ) -> None:
        raise NothingToAddError

    @abstractmethod
    async def recover(self, position_id: PositionId, ids: Sequence[UUID]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def archive(self, ids: Sequence[UUID], now: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_availability(
        self, position_id: PositionId, amount: ItemsAmount
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, ids: Sequence[UUID]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _add(
        self,
        creator_id: UserId,
        position_id: PositionId,
        contents: Sequence[ItemContent],
    ) -> tuple[ItemSnapshot, ...]:
        raise NotImplementedError


class FixedWarehouse(Warehouse):
    def __init__(self, repo: FixedItemRepository, factory: FixedItemFactory):
        self._repo = repo
        self._factory = factory

    @override
    async def _add(
        self,
        creator_id: UserId,
        position_id: PositionId,
        contents: Sequence[ItemContent],
    ) -> tuple[ItemSnapshot, ...]:
        available_item: list[FixedItem] = await self._repo.get_by_position_id(
            position_id=position_id, status=FixedItemStatus.AVAILABLE
        )

        if available_item or len(contents) > 1:
            raise PositionWarehouseFullError

        item: FixedItem = self._factory.create(
            creator_id=creator_id, position_id=position_id, content=contents[0]
        )

        await self._repo.add(item=item)
        return (item.take_snapshot(),)

    @override
    async def replace(
        self, item_id: UUID, new_content: ItemContent, now: datetime
    ) -> None:
        item: FixedItem | None = await self._repo.get(
            item_id=FixedItemId(value=item_id)
        )
        if not item:
            raise FixedItemNotFoundError

        item.replace_content(new_content=new_content, now=now)

    @override
    async def recover(self, position_id: PositionId, ids: Sequence[UUID]) -> None:
        current_items: list[FixedItem] = await self._repo.get_by_position_id(
            position_id=position_id, status=FixedItemStatus.AVAILABLE
        )
        if current_items:
            raise PositionWarehouseFullError

        item: FixedItem | None = await self._repo.get(item_id=FixedItemId(ids[0]))
        if not item:
            raise FixedItemNotFoundError

        item.recover()

    @override
    async def archive(self, ids: Sequence[UUID], now: datetime) -> None:
        item: FixedItem | None = await self._repo.get(item_id=FixedItemId(ids[0]))
        if not item:
            raise FixedItemNotFoundError

        item.archive(now=now)

    @override
    async def check_availability(
        self, position_id: PositionId, amount: ItemsAmount
    ) -> None:
        current_items: list[FixedItem] = await self._repo.get_by_position_id(
            position_id=position_id, status=FixedItemStatus.AVAILABLE
        )
        if len(current_items) < amount.value:
            raise OutOfStockError(available=len(current_items))

    @override
    async def delete(self, ids: Sequence[UUID]) -> None:
        item: FixedItem | None = await self._repo.get(item_id=FixedItemId(ids[0]))
        if not item:
            raise FixedItemNotFoundError
        item.ensure_can_delete()
        await self._repo.delete(item=item)


class UnlimitedWarehouse(Warehouse):
    def __init__(self, repo: StockItemRepository, factory: StockItemFactory):
        self._repo = repo
        self._factory = factory

    @override
    async def _add(
        self,
        creator_id: UserId,
        position_id: PositionId,
        contents: Sequence[ItemContent],
    ) -> tuple[ItemSnapshot, ...]:
        items: tuple[StockItem, ...] = self._factory.create(
            creator_id=creator_id, position_id=position_id, contents=contents
        )

        await self._repo.add_many(items=items)
        return tuple(item.take_snapshot() for item in items)

    @override
    async def replace(
        self, item_id: UUID, new_content: ItemContent, now: datetime
    ) -> None:
        item: StockItem | None = await self._repo.get(
            item_id=StockItemId(value=item_id)
        )
        if not item:
            raise StockItemNotFoundError

        item.replace_content(new_content=new_content, now=now)

    @override
    async def recover(self, position_id: PositionId, ids: Sequence[UUID]) -> None:
        items: list[StockItem] = await self._repo.acquire_by_ids(
            ids=[StockItemId(id_) for id_ in ids]
        )
        for item in items:
            item.recover()

    @override
    async def archive(self, ids: Sequence[UUID], now: datetime) -> None:
        items: list[StockItem] = await self._repo.acquire_by_ids(
            ids=[StockItemId(id_) for id_ in ids]
        )
        for item in items:
            item.archive(now=now)

    @override
    async def check_availability(
        self, position_id: PositionId, amount: ItemsAmount
    ) -> None:
        current: int = await self._repo.count_items(
            position_id=position_id, status=StockItemStatus.AVAILABLE
        )
        if current < amount.value:
            raise OutOfStockError(available=current)

    @override
    async def delete(self, ids: Sequence[UUID]) -> None:
        items: list[StockItem] = await self._repo.acquire_by_ids(
            ids=[StockItemId(id_) for id_ in ids]
        )
        for item in items:
            item.ensure_can_delete()
            await self._repo.delete(item=item)
