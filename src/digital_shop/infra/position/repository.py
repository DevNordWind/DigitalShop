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
from domain.product.position.port import PositionRepository
from domain.product.position.value_object import PositionId
from infra.framework.sql_alchemy.table.position import (
    ItemType,
    item_table,
    position_table,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class PositionRepositoryImpl(PositionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, position: Position) -> None:
        self._session.add(position)

    async def add_item(self, item: Item) -> None:
        self._session.add(item)

    async def add_items(self, items: Sequence[Item]) -> None:
        self._session.add_all(items)

    async def get(self, position_id: PositionId) -> Position | None:
        stmt = select(Position).where(position_table.c.id == position_id.value)
        result = await self._session.scalar(stmt)

        return result or None

    async def get_for_update(self, position_id: PositionId) -> Position | None:
        stmt = (
            select(Position)
            .where(position_table.c.id == position_id.value)
            .with_for_update()
        )
        result = await self._session.scalar(stmt)

        return result or None

    async def get_items_for_update(
        self,
        position_id: PositionId,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        stmt = select(Item).where(
            item_table.c.position_id == position_id.value,
        )
        if status is not None:
            stmt = stmt.where(item_table.c.status == status)

        stmt = stmt.with_for_update()
        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def get_item_for_update(self, item_id: ItemId) -> Item | None:
        stmt = (
            select(Item)
            .where(item_table.c.id == item_id.value)
            .with_for_update()
        )
        result = await self._session.scalar(stmt)

        return result or None

    async def get_finite_items_by_ids(
        self,
        items_ids: Sequence[ItemId],
    ) -> list[FiniteItem]:
        stmt = select(Item).where(
            item_table.c.type == ItemType.FINITE,
            item_table.c.id.in_([i.value for i in items_ids]),
        )
        results = (await self._session.scalars(stmt)).all()

        return list(results)  # type: ignore[arg-type]

    async def get_items_for_update_by_category_ids(
        self,
        category_ids: Sequence[CategoryId],
        status: ItemStatus | None = None,
    ) -> list[Item]:
        stmt = select(Item).where(
            position_table.c.category_id.in_([c.value for c in category_ids]),
        )
        if status is not None:
            stmt = stmt.where(item_table.c.status == status)

        stmt = stmt.join(
            position_table,
            position_table.c.id == item_table.c.position_id,
        ).with_for_update()

        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def get_by_category_ids_for_update(
        self,
        category_ids: Sequence[CategoryId],
        status: PositionStatus | None = None,
    ) -> list[Position]:
        stmt = select(Position).where(
            position_table.c.category_id.in_([c.value for c in category_ids]),
        )
        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        stmt = stmt.with_for_update()
        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def acquire_items(
        self,
        position_id: PositionId,
        amount: ItemsAmount,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        stmt = select(Item).where(
            item_table.c.position_id == position_id.value,
        )
        if status is not None:
            stmt = stmt.where(item_table.c.status == status)

        stmt = stmt.limit(amount.value)
        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def acquire_items_for_update(
        self,
        position_id: PositionId,
        amount: ItemsAmount,
        status: ItemStatus | None = None,
    ) -> list[Item]:
        stmt = select(Item).where(
            item_table.c.position_id == position_id.value,
        )
        if status is not None:
            stmt = stmt.where(item_table.c.status == status)

        stmt = stmt.limit(amount.value).with_for_update(skip_locked=True)
        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def get_item_category_id(self, item_id: ItemId) -> CategoryId | None:
        stmt = (
            select(position_table.c.category_id)
            .join(item_table, item_table.c.position_id == position_table.c.id)
            .where(item_table.c.id == item_id.value)
        )
        result = await self._session.scalar(stmt)

        return CategoryId(result) if result else None

    async def delete(self, position: Position) -> None:
        await self._session.delete(position)

    async def delete_item(self, item: Item) -> None:
        await self._session.delete(item)

    async def count_items(
        self,
        position_id: PositionId,
        status: ItemStatus | None = ItemStatus.AVAILABLE,
    ) -> int:
        stmt = select(func.count(item_table.c.id)).where(
            item_table.c.position_id == position_id.value,
        )
        if status is not None:
            stmt = stmt.where(item_table.c.status == status)
        result = await self._session.scalar(stmt)

        return result or 0
