from app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.product.category.dto.category import (
    CategoryDTO,
    CategoryShortDTO,
    CategoryWithGoodsAmountDTO,
)
from app.product.category.dto.paginated import (
    CategoriesPaginated,
    CategoriesShortPaginated,
)
from app.product.category.dto.sorting import CategorySortingParams
from app.product.category.port import CategoryReader
from domain.product.category.enums import CategoryStatus
from domain.product.category.value_object import CategoryId
from infra.category.reader.mapper import CategoryReaderMapper
from infra.category.reader.select import SELECT_CATEGORY, SELECT_SHORT_CATEGORY
from infra.category.reader.subq import (
    ITEM_EXISTS_SUBQ,
    ITEMS_COUNT_SUBQ,
    POSITION_COUNT_SUBQ,
)
from infra.framework.sql_alchemy.table.category import category_table
from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryReaderImpl(CategoryReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read(self, category_id: CategoryId) -> CategoryDTO | None:
        stmt = (
            select(*SELECT_CATEGORY)
            .where(category_table.c.id == category_id.value)
            .limit(1)
        )

        result = await self._session.execute(stmt)
        row = result.first()

        if not row:
            return None

        return CategoryReaderMapper.to_dto(row=row)

    async def read_with_goods_amount(
        self,
        category_id: CategoryId,
    ) -> CategoryWithGoodsAmountDTO | None:
        stmt = select(
            category_table,
            POSITION_COUNT_SUBQ.label("positions_amount"),
            ITEMS_COUNT_SUBQ.label("items_amount"),
        ).where(category_table.c.id == category_id.value)

        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return CategoryWithGoodsAmountDTO(
            category=CategoryReaderMapper.to_dto(row=row),
            positions_amount=row.positions_amount or 0,
            items_amount=row.items_amount or 0,
        )

    async def read_short(
        self,
        category_id: CategoryId,
    ) -> CategoryShortDTO | None:
        stmt = select(*SELECT_SHORT_CATEGORY).where(
            category_table.c.id == category_id.value,
        )

        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return CategoryReaderMapper.to_short_dto(row=row)

    async def read_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        status: CategoryStatus | None,
    ) -> CategoriesPaginated:
        sorting_col = category_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *SELECT_CATEGORY,
            func.count().over().label("total"),
        )
        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        stmt = (
            stmt.order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return CategoriesPaginated(categories=[], total=0)

        total = rows[0].total

        return CategoriesPaginated(
            categories=[CategoryReaderMapper.to_dto(row=row) for row in rows],
            total=total,
        )

    async def read_short_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        show_with_no_items: bool | None,
        status: CategoryStatus | None,
    ) -> CategoriesShortPaginated:
        sorting_col = category_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *SELECT_SHORT_CATEGORY,
            func.count().over().label("total"),
        )

        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        if show_with_no_items is False:
            stmt = stmt.where(exists(ITEM_EXISTS_SUBQ))

        stmt = (
            stmt.order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return CategoriesShortPaginated(categories=[], total=0)

        total = rows[0].total

        return CategoriesShortPaginated(
            categories=[
                CategoryReaderMapper.to_short_dto(row) for row in rows
            ],
            total=total,
        )
