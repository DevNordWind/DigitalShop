from typing import Any, override

from sqlalchemy import Column, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.shopping.category.dto.category import (
    CategoryDTO,
    CategoryShortDTO,
    CategoryWithGoodsAmountDTO,
)
from app.app.shopping.category.dto.paginated import (
    CategoriesPaginated,
    CategoriesShortPaginated,
)
from app.app.shopping.category.dto.sorting import CategorySortingParams
from app.app.shopping.category.port import CategoryReader
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.value_object import CategoryId
from app.infra.framework.sql_alchemy.table.category import category_table
from app.infra.shopping.category.reader.mapper import CategoryReaderMapper
from app.infra.shopping.category.reader.select import (
    CATEGORY_SELECT,
    CATEGORY_SHORT_SELECT,
)
from app.infra.shopping.category.reader.subq import (
    CATEGORY_HAS_POSITIONS_SUBQ,
    ITEMS_COUNT_SUBQ,
    POSITIONS_COUNT_SUBQ,
)


class SqlACategoryReader(CategoryReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def read(self, category_id: CategoryId) -> CategoryDTO | None:
        stmt = select(*CATEGORY_SELECT).where(category_table.c.id == category_id)
        row = (await self._session.execute(stmt)).first()
        return CategoryReaderMapper.to_dto(row=row) if row else None

    @override
    async def read_short(self, category_id: CategoryId) -> CategoryShortDTO | None:
        stmt = select(*CATEGORY_SHORT_SELECT).where(category_table.c.id == category_id)
        row = (await self._session.execute(stmt)).first()
        return CategoryReaderMapper.to_short_dto(row=row) if row else None

    @override
    async def read_with_goods_amount(
        self, category_id: CategoryId
    ) -> CategoryWithGoodsAmountDTO | None:
        stmt = select(
            *CATEGORY_SELECT,
            POSITIONS_COUNT_SUBQ,
            ITEMS_COUNT_SUBQ,
        ).where(category_table.c.id == category_id)

        row = (await self._session.execute(stmt)).first()
        return CategoryReaderMapper.to_with_goods_amount_dto(row=row) if row else None

    @override
    async def read_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        status: CategoryStatus | None,
    ) -> CategoriesPaginated:
        stmt = self._build_category_query(
            select_columns=CATEGORY_SELECT,
            sorting=sorting,
            pagination=pagination,
            status=status,
            show_with_no_items=None,
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return CategoriesPaginated(categories=[], total=0)

        return CategoriesPaginated(
            categories=[CategoryReaderMapper.to_dto(row=row) for row in rows],
            total=rows[0].total,
        )

    @override
    async def read_short_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        show_with_no_items: bool | None,
        status: CategoryStatus | None,
    ) -> CategoriesShortPaginated:
        stmt = self._build_category_query(
            select_columns=CATEGORY_SHORT_SELECT,
            sorting=sorting,
            pagination=pagination,
            status=status,
            show_with_no_items=show_with_no_items,
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return CategoriesShortPaginated(categories=[], total=0)

        return CategoriesShortPaginated(
            categories=[CategoryReaderMapper.to_short_dto(row=row) for row in rows],
            total=rows[0].total,
        )

    def _build_category_query(
        self,
        select_columns: tuple[Column[Any], ...],
        sorting: CategorySortingParams,
        pagination: OffsetPaginationParams,
        status: CategoryStatus | None,
        show_with_no_items: bool | None,
    ) -> Select[Any]:
        sorting_col = category_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(*select_columns, func.count().over().label("total"))

        if status is not None:
            stmt = stmt.where(category_table.c.status == status)

        if show_with_no_items is False:
            stmt = stmt.where(CATEGORY_HAS_POSITIONS_SUBQ)

        return stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)
