from collections.abc import Sequence
from datetime import datetime

from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import (
    OutOfStock,
    PositionPermissionDenied,
)
from domain.product.position.item.entity import FiniteItem, Item
from domain.product.position.item.enums import (
    ItemStatus,
)
from domain.product.position.item.factory import ItemFactory
from domain.product.position.item.value_object import ItemId, ItemRaw
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.strategy import (
    FiniteWarehouse,
    InfiniteWarehouse,
)
from domain.user.entity import User


class PositionWarehouseService:
    def __init__(
        self,
        repository: PositionRepository,
        clock: Clock,
        item_factory: ItemFactory,
    ):
        self._repository: PositionRepository = repository
        self._clock: Clock = clock
        self._item_factory: ItemFactory = item_factory

    async def add_item(
        self,
        creator: User,
        position: Position,
        item_raw: ItemRaw,
    ) -> Item:
        await self.__before_add_item(
            creator=creator,
            position=position,
            to_add=1,
        )

        return self._item_factory.create(
            position=position,
            creator_id=creator.id,
            item_raw=item_raw,
            now=self._clock.now(),
        )

    async def add_items(
        self,
        creator: User,
        position: Position,
        items_raw: Sequence[ItemRaw],
    ) -> list[Item]:
        await self.__before_add_item(
            creator=creator,
            position=position,
            to_add=len(items_raw),
        )
        now: datetime = self._clock.now()

        return [
            self._item_factory.create(
                position=position,
                creator_id=creator.id,
                item_raw=item_raw,
                now=now,
            )
            for item_raw in items_raw
        ]

    async def check_availability(
        self,
        position: Position,
        amount: ItemsAmount,
    ) -> None:
        count: int = await self._repository.count_items(
            position_id=position.id,
            status=ItemStatus.AVAILABLE,
        )
        if count < amount.value:
            raise OutOfStock(available=count)

    async def acquire_for_reserve(
        self,
        position: Position,
        amount: ItemsAmount,
    ) -> list[Item]:
        position.ensure_can_acquire()
        now: datetime = self._clock.now()
        items: list[Item]

        match position.warehouse:
            case InfiniteWarehouse():
                items = await self._repository.acquire_items(
                    position_id=position.id,
                    amount=amount,
                    status=ItemStatus.AVAILABLE,
                )
            case FiniteWarehouse():
                items = await self._repository.acquire_items_for_update(
                    position_id=position.id,
                    amount=amount,
                    status=ItemStatus.AVAILABLE,
                )
                for item in items:
                    if not isinstance(item, FiniteItem):
                        raise ValueError(
                            "Incompatible item type for FiniteWarehouse",
                        )
                    position.warehouse.acquire(item=item, now=now)
            case _:
                raise ValueError(
                    f"Unknown warehouse type: {type(position.warehouse)}",
                )

        if len(items) < amount.value:
            raise OutOfStock(available=len(items))

        return items

    async def acquire_for_sell(
        self,
        position: Position,
        amount: ItemsAmount,
    ) -> list[Item]:
        now: datetime = self._clock.now()
        items: list[Item]

        match position.warehouse:
            case InfiniteWarehouse():
                items = await self._repository.acquire_items(
                    position_id=position.id,
                    amount=amount,
                    status=ItemStatus.AVAILABLE,
                )
            case FiniteWarehouse():
                items = await self._repository.acquire_items_for_update(
                    position_id=position.id,
                    amount=amount,
                    status=ItemStatus.AVAILABLE,
                )
                for item in items:
                    if not isinstance(item, FiniteItem):
                        raise ValueError(
                            "Incompatible item type for FiniteWarehouse",
                        )
                    item.sell_direct(now=now)
            case _:
                raise ValueError(
                    f"Unknown warehouse type: {type(position.warehouse)}",
                )

        if len(items) < amount.value:
            raise OutOfStock(available=len(items))

        return items

    async def release_reserved(self, items_ids: Sequence[ItemId]) -> None:
        items: list[
            FiniteItem
        ] = await self._repository.get_finite_items_by_ids(items_ids=items_ids)
        for item in items:
            item.release()

    async def sell_reserved(
        self,
        items_ids: Sequence[ItemId],
        now: datetime,
    ) -> None:
        items: list[
            FiniteItem
        ] = await self._repository.get_finite_items_by_ids(items_ids=items_ids)
        for item in items:
            item.sell_reserved(now)

    async def recover_item(
        self,
        position: Position,
        item: Item,
    ) -> None:
        current: int = await self._repository.count_items(
            position_id=position.id,
        )
        position.ensure_can_add_item(current=current, to_add=1)
        item.recover()

    async def __before_add_item(
        self,
        creator: User,
        position: Position,
        to_add: int,
    ) -> None:
        if not PositionAccessService.can_add_item(creator_role=creator.role):
            raise PositionPermissionDenied

        count: int = await self._repository.count_items(
            position_id=position.id,
        )

        position.ensure_can_add_item(current=count, to_add=to_add)
