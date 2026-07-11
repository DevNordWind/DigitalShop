from collections.abc import Sequence
from uuid import UUID

from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.factory import (
    WarehouseFactory,
)
from app.domain.shopping.position.item.value_object import (
    ItemContent,
    ItemsAmount,
    ItemSnapshot,
)
from app.domain.shopping.position.strategy import Warehouse
from app.domain.user.value_object import UserId


class PositionWarehouseDomainService:
    def __init__(self, warehouse_factory: WarehouseFactory, clock: Clock):
        self._warehouse_factory = warehouse_factory
        self._clock = clock

    async def add(
        self, creator_id: UserId, position: Position, contents: Sequence[ItemContent]
    ) -> tuple[ItemSnapshot, ...]:
        position.ensure_not_archived()
        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )

        return await warehouse.add(
            creator_id=creator_id, position_id=position.id, contents=contents
        )

    async def recover(self, position: Position, ids: Sequence[UUID]) -> None:
        position.ensure_not_archived()
        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )
        await warehouse.recover(position_id=position.id, ids=ids)

    async def archive(self, position: Position, ids: Sequence[UUID]) -> None:
        position.ensure_not_archived()

        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )
        await warehouse.archive(ids=ids, now=self._clock.now())

    async def replace(
        self, position: Position, item_id: UUID, new_content: ItemContent
    ) -> None:
        position.ensure_not_archived()

        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )
        await warehouse.replace(
            item_id=item_id, new_content=new_content, now=self._clock.now()
        )

    async def delete(self, position: Position, ids: Sequence[UUID]) -> None:
        position.ensure_not_archived()

        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )
        await warehouse.delete(ids=ids)

    async def check_availability(self, position: Position, amount: ItemsAmount) -> None:
        position.ensure_not_archived()
        warehouse: Warehouse = await self._warehouse_factory.create(
            tp=position.warehouse_type
        )
        await warehouse.check_availability(position_id=position.id, amount=amount)
