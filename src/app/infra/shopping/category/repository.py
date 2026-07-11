from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.value_object import CategoryId
from app.infra.framework.sql_alchemy.table.category import category_table


class SqlACategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, category: Category) -> None:
        self._session.add(category)

    @override
    async def get(self, category_id: CategoryId) -> Category | None:
        stmt = select(Category).where(category_table.c.id == category_id).limit(1)
        return await self._session.scalar(stmt)

    @override
    async def get_by_status(
        self,
        status: CategoryStatus | None = None,
    ) -> list[Category]:
        stmt = select(Category)
        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        result = await self._session.scalars(stmt)

        return list(result.all())

    @override
    async def acquire(self, category_id: CategoryId) -> Category | None:
        stmt = (
            select(Category).where(category_table.c.id == category_id).with_for_update()
        )
        return await self._session.scalar(stmt)

    @override
    async def acquire_all_by_status(
        self, status: CategoryStatus | None = None
    ) -> list[Category]:
        stmt = select(Category).with_for_update()
        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        result = await self._session.scalars(stmt)

        return list(result.all())

    @override
    async def delete(self, category: Category) -> None:
        await self._session.delete(category)
