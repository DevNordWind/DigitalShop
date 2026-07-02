from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import override

from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import OutOfStockError
from app.domain.shopping.position.item.entity import FixedItem, StockItem
from app.domain.shopping.position.item.enums import FixedItemStatus, StockItemStatus
from app.domain.shopping.position.item.port import (
    FixedItemRepository,
    StockItemRepository,
)
from app.domain.shopping.position.item.value_object import (
    ItemSnapshot,
    StockItemId,
)
from app.domain.shopping.position.value_object import HoldContext, SellContext


class FulfillmentStrategy(ABC):
    @abstractmethod
    async def hold(
        self, position: Position, ctx: HoldContext
    ) -> tuple[ItemSnapshot, ...]:
        raise NotImplementedError

    @abstractmethod
    async def sell(self, snapshots: Sequence[ItemSnapshot], ctx: SellContext) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self, snapshots: Sequence[ItemSnapshot]) -> None:
        raise NotImplementedError


class StockFulfillment(FulfillmentStrategy):
    def __init__(self, repo: StockItemRepository):
        self._repo = repo

    @override
    async def hold(
        self, position: Position, ctx: HoldContext
    ) -> tuple[ItemSnapshot, ...]:
        items: list[StockItem] = await self._repo.acquire_by_position_id(
            position_id=position.id, amount=ctx.amount, status=StockItemStatus.AVAILABLE
        )
        if len(items) < ctx.amount.value:
            raise OutOfStockError(available=len(items))

        snapshots: list[ItemSnapshot] = []
        for item in items:
            item.reserve(now=ctx.now)
            snapshots.append(item.take_snapshot())

        return tuple(snapshots)

    @override
    async def sell(self, snapshots: Sequence[ItemSnapshot], ctx: SellContext) -> None:
        items: list[StockItem] = await self._repo.acquire_by_ids(
            ids=[StockItemId(snap.id) for snap in snapshots]
        )
        for item in items:
            item.sell(now=ctx.now)

    @override
    async def rollback(self, snapshots: Sequence[ItemSnapshot]) -> None:
        items: list[StockItem] = await self._repo.acquire_by_ids(
            ids=[StockItemId(snap.id) for snap in snapshots]
        )
        for item in items:
            item.release()


class FixedFulfillment(FulfillmentStrategy):
    def __init__(self, repo: FixedItemRepository):
        self._repo = repo

    @override
    async def hold(
        self, position: Position, ctx: HoldContext
    ) -> tuple[ItemSnapshot, ...]:
        items: list[FixedItem] = await self._repo.get_by_position_id(
            position_id=position.id, status=FixedItemStatus.AVAILABLE
        )
        if not items or ctx.amount.value > 1:
            raise OutOfStockError(available=len(items))

        return (items[0].take_snapshot(),)

    @override
    async def sell(self, snapshots: Sequence[ItemSnapshot], ctx: SellContext) -> None:
        """No-op: Confirmation isn't required"""
        pass

    @override
    async def rollback(self, snapshots: Sequence[ItemSnapshot]) -> None:
        """No-op: Rollback isn't required"""
        pass
