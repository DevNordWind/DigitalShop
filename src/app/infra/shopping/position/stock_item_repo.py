from collections.abc import Sequence
from typing import override

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shopping.position.item.entity import StockItem
from app.domain.shopping.position.item.enums import StockItemStatus
from app.domain.shopping.position.item.port import StockItemRepository
from app.domain.shopping.position.item.value_object import ItemsAmount, StockItemId
from app.domain.shopping.position.value_object import PositionId
from app.infra.framework.sql_alchemy.table.position import (
    position_table,
    stock_item_table,
)


class SqlAStockItemRepository(StockItemRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def add_many(self, items: Sequence[StockItem]) -> None:
        self._session.add_all(items)

    @override
    async def get(self, item_id: StockItemId) -> StockItem | None:
        stmt = select(StockItem).where(stock_item_table.c.id == item_id).limit(1)

        return await self._session.scalar(stmt)

    @override
    async def acquire_by_position_id(
        self,
        position_id: PositionId,
        amount: ItemsAmount | None = None,
        status: StockItemStatus | None = None,
    ) -> list[StockItem]:
        stmt = (
            select(StockItem)
            .join(position_table, position_table.c.id == stock_item_table.c.position_id)
            .where(position_table.c.id == position_id)
            .with_for_update(skip_locked=True)
        )
        if status is not None:
            stmt = stmt.where(stock_item_table.c.status == status)
        if amount is not None:
            stmt = stmt.limit(amount.value)

        result = await self._session.scalars(stmt)
        return list(result.all())

    @override
    async def acquire_by_ids(
        self,
        ids: Sequence[StockItemId],
    ) -> list[StockItem]:
        stmt = select(StockItem).where(stock_item_table.c.id.in_(ids)).with_for_update()

        result = await self._session.scalars(stmt)
        return list(result.all())

    @override
    async def count_items(
        self,
        position_id: PositionId,
        status: StockItemStatus | None = None,
    ) -> int:
        stmt = (
            select(func.count(stock_item_table.c.id))
            .join(position_table, position_table.c.id == stock_item_table.c.position_id)
            .where(position_table.c.id == position_id)
        )
        if status is not None:
            stmt = stmt.where(stock_item_table.c.status == status)

        return await self._session.scalar(stmt) or 0

    @override
    async def delete(self, item: StockItem) -> None:
        await self._session.delete(item)
