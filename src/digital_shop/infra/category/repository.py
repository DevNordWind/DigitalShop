from domain.product.category.entity import Category
from domain.product.category.enums import CategoryStatus
from domain.product.category.port import CategoryRepository
from domain.product.category.value_object import CategoryId
from infra.framework.sql_alchemy.table.category import category_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepositoryImpl(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, category: Category) -> None:
        self._session.add(category)

    async def get(self, category_id: CategoryId) -> Category | None:
        stmt = (
            select(Category)
            .where(category_table.c.id == category_id.value)
            .limit(1)
        )
        result = await self._session.scalar(stmt)
        if not result:
            return None

        return result

    async def get_all(
        self,
        status: CategoryStatus | None = None,
    ) -> list[Category]:
        stmt = select(Category)
        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        results = (await self._session.scalars(stmt)).all()

        return list(results)

    async def delete(self, category: Category) -> None:
        await self._session.delete(category)
