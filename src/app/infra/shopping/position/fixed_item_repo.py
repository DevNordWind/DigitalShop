from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shopping.position.item.entity import FixedItem
from app.domain.shopping.position.item.enums import FixedItemStatus
from app.domain.shopping.position.item.port import (
    FixedItemRepository,
)
from app.domain.shopping.position.item.value_object import FixedItemId
from app.domain.shopping.position.value_object import PositionId
from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
)


class SqlAFixedItemRepository(FixedItemRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def add(self, item: FixedItem) -> None:
        self._session.add(item)

    @override
    async def get(self, item_id: FixedItemId) -> FixedItem | None:
        stmt = select(FixedItem).where(fixed_item_table.c.id == item_id).limit(1)

        return await self._session.scalar(stmt)

    @override
    async def get_by_position_id(
        self, position_id: PositionId, status: FixedItemStatus | None = None
    ) -> list[FixedItem]:
        stmt = (
            select(FixedItem)
            .join(position_table, position_table.c.id == fixed_item_table.c.position_id)
            .where(position_table.c.id == position_id)
        )
        if status is not None:
            stmt = stmt.where(fixed_item_table.c.status == status)

        result = await self._session.scalars(stmt)
        return list(result.all())

    @override
    async def delete(self, item: FixedItem) -> None:
        await self._session.delete(item)
