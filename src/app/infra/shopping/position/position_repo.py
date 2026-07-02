from collections.abc import Sequence
from typing import override
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import (
    FulfillmentType,
    PositionStatus,
)
from app.domain.shopping.position.item.enums import (
    FixedItemStatus,
    GenericItemStatus,
    StockItemStatus,
)
from app.domain.shopping.position.item.value_object import FixedItemId, StockItemId
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.value_object import PositionId
from app.infra.framework.sql_alchemy.table.category import category_table
from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)


class SqlAPositionRepository(PositionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def add(self, position: Position) -> None:
        self._session.add(position)

    @override
    async def get(self, position_id: PositionId) -> Position | None:
        stmt = select(Position).where(position_table.c.id == position_id)
        return await self._session.scalar(stmt)

    @override
    async def get_by_item_id(
        self,
        item_id: UUID,
    ) -> Position | None:
        stock_result: Position | None = await self._get_by_stock(
            item_id=StockItemId(item_id)
        )
        if stock_result:
            return stock_result

        return await self._get_by_fixed(item_id=FixedItemId(item_id))

    @override
    async def get_with_items_ids(
        self,
        position_id: PositionId,
        item_status: GenericItemStatus | None = None,
    ) -> tuple[Position | None, tuple[UUID, ...]]:
        stmt = select(Position).where(position_table.c.id == position_id)
        result: Position | None = await self._session.scalar(stmt)
        if not result:
            return None, ()

        match result.fulfillment_type:
            case FulfillmentType.FIXED:
                items_ids = await self._get_fixed_item_ids(
                    position_id=position_id, item_status=item_status
                )
            case FulfillmentType.STOCK:
                items_ids = await self._get_stock_item_ids(
                    position_id=position_id, item_status=item_status
                )

        return result, items_ids

    @override
    async def get_by_category_ids_status(
        self, category_ids: Sequence[CategoryId], status: PositionStatus | None = None
    ) -> list[Position]:
        stmt = (
            select(Position)
            .join(category_table, position_table.c.category_id == category_table.c.id)
            .where(category_table.c.id.in_(category_ids))
        )
        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        result = await self._session.scalars(stmt)
        return list(result.all())

    @override
    async def acquire(self, position_id: PositionId) -> Position | None:
        stmt = (
            select(Position).where(position_table.c.id == position_id).with_for_update()
        )
        return await self._session.scalar(stmt)

    @override
    async def acquire_by_category_ids_status(
        self, category_ids: Sequence[CategoryId], status: PositionStatus | None = None
    ) -> list[Position]:
        stmt = (
            select(Position)
            .join(category_table, position_table.c.category_id == category_table.c.id)
            .where(category_table.c.id.in_(category_ids))
            .with_for_update()
        )
        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        result = await self._session.scalars(stmt)
        return list(result.all())

    @override
    async def delete(self, position: Position) -> None:
        await self._session.delete(position)

    async def _get_by_stock(self, item_id: StockItemId) -> Position | None:
        stmt = (
            select(Position)
            .join(
                stock_item_table, position_table.c.id == stock_item_table.c.position_id
            )
            .where(stock_item_table.c.id == item_id)
        )
        return await self._session.scalar(stmt)

    async def _get_by_fixed(self, item_id: FixedItemId) -> Position | None:
        stmt = (
            select(Position)
            .join(
                fixed_item_table, position_table.c.id == fixed_item_table.c.position_id
            )
            .where(fixed_item_table.c.id == item_id)
        )
        return await self._session.scalar(stmt)

    async def _get_stock_item_ids(
        self,
        position_id: PositionId,
        item_status: GenericItemStatus | None,
    ) -> tuple[UUID, ...]:
        stmt = select(stock_item_table.c.id).where(
            stock_item_table.c.position_id == position_id.value
        )
        if item_status is not None:
            stmt = stmt.where(
                stock_item_table.c.status == StockItemStatus(item_status.value)
            )

        result = await self._session.execute(stmt)
        return tuple(row[0] for row in result.all())

    async def _get_fixed_item_ids(
        self,
        position_id: PositionId,
        item_status: GenericItemStatus | None,
    ) -> tuple[UUID, ...]:
        stmt = select(fixed_item_table.c.id).where(
            fixed_item_table.c.position_id == position_id.value
        )
        if item_status is not None:
            stmt = stmt.where(
                fixed_item_table.c.status == FixedItemStatus(item_status.value)
            )

        result = await self._session.execute(stmt)
        return tuple(row[0] for row in result.all())
