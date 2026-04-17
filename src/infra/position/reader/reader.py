from sqlalchemy import (
    exists,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.product.position.dto.item import (
    ItemDTO,
)
from app.product.position.dto.paginated import (
    PositionItemsPaginated,
    PositionsPaginated,
    PositionsShortPaginated,
    PositionWithItemsAmountPaginated,
)
from app.product.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionWithItemsAmount,
)
from app.product.position.dto.sorting import (
    PositionItemsSortingParams,
    PositionSortingParams,
)
from app.product.position.port import PositionReader
from domain.product.category.value_object import CategoryId
from domain.product.position.enums import PositionStatus
from domain.product.position.item.enums import (
    ItemStatus,
)
from domain.product.position.item.value_object import ItemId
from domain.product.position.value_object import PositionId
from infra.framework.sql_alchemy.table.position import (
    item_table,
    position_table,
)
from infra.position.reader.mapper import PositionReaderMapper
from infra.position.reader.select import (
    ITEM_SELECT,
    POSITION_SELECT,
    POSITION_SHORT_SELECT,
)
from infra.position.reader.subq import ITEM_EXISTS_SUBQ, ITEMS_COUNT_SUBQ


class PositionReaderImpl(PositionReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read(self, position_id: PositionId) -> PositionDTO | None:
        stmt = select(*POSITION_SELECT).where(
            position_table.c.id == position_id.value,
        )
        result = await self._session.execute(stmt)
        row = result.first()

        if not row:
            return None

        return PositionReaderMapper.to_dto(row=row)

    async def read_short(
        self,
        position_id: PositionId,
    ) -> PositionShortDTO | None:
        stmt = select(*POSITION_SHORT_SELECT).where(
            position_table.c.id == position_id.value,
        )
        result = await self._session.execute(stmt)
        row = result.first()

        if not row:
            return None

        return PositionReaderMapper.to_short_dto(row=row)

    async def read_with_items_amount(
        self,
        position_id: PositionId,
    ) -> PositionWithItemsAmount | None:
        stmt = select(
            *POSITION_SELECT,
            ITEMS_COUNT_SUBQ.label("items_amount"),
        ).where(position_table.c.id == position_id.value)

        result = await self._session.execute(stmt)
        row = result.first()

        if not row:
            return None

        return PositionWithItemsAmount(
            position=PositionReaderMapper.to_dto(row),
            items_amount=row.items_amount or 0,
        )

    async def read_short_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        show_with_no_items: bool | None,
        status: PositionStatus | None,
    ) -> PositionsShortPaginated:
        sorting_col = position_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *POSITION_SHORT_SELECT,
            func.count().over().label("total"),
        ).where(position_table.c.category_id == category_id.value)

        if show_with_no_items is False:
            stmt = stmt.where(exists(ITEM_EXISTS_SUBQ))

        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        stmt = (
            stmt.order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return PositionsShortPaginated(positions=[], total=0)

        total = rows[0].total

        return PositionsShortPaginated(
            positions=[PositionReaderMapper.to_short_dto(row) for row in rows],
            total=total,
        )

    async def read_with_items_amount_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> PositionWithItemsAmountPaginated:
        sorting_col = position_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = (
            select(
                *POSITION_SELECT,
                func.count(item_table.c.id).label("items_amount"),
                func.count().over().label("total"),
            )
            .outerjoin(
                item_table, item_table.c.position_id == position_table.c.id
            )
            .where(position_table.c.category_id == category_id.value)
        )

        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        if show_with_no_items is False:
            stmt = stmt.having(func.count(item_table.c.id) > 0)

        stmt = (
            stmt.group_by(*POSITION_SELECT)
            .order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return PositionWithItemsAmountPaginated(positions=[], total=0)

        total = rows[0].total

        return PositionWithItemsAmountPaginated(
            positions=[
                PositionWithItemsAmount(
                    position=PositionReaderMapper.to_dto(row=row),
                    items_amount=row.items_amount,
                )
                for row in rows
            ],
            total=total,
        )

    async def read_all_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> PositionsPaginated:
        sorting_col = position_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *POSITION_SELECT,
            func.count().over().label("total"),
        ).where(position_table.c.category_id == category_id.value)

        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

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
            return PositionsPaginated(positions=[], total=0)

        total = rows[0].total

        return PositionsPaginated(
            positions=[PositionReaderMapper.to_dto(row) for row in rows],
            total=total,
        )

    async def read_item(self, item_id: ItemId) -> ItemDTO | None:
        stmt = select(*ITEM_SELECT).where(item_table.c.id == item_id.value)
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return PositionReaderMapper.to_item_dto(row=row)

    async def read_position_items_by_warehouse(
        self,
        position_id: PositionId,
        sorting: PositionItemsSortingParams,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        sorting_col = item_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *ITEM_SELECT,
            func.count().over().label("total"),
        ).where(item_table.c.position_id == position_id.value)

        if status is not None:
            stmt = stmt.where(item_table.c.status == status)

        stmt = (
            stmt.order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return PositionItemsPaginated(items=[], total=0)

        return PositionItemsPaginated(
            items=[PositionReaderMapper.to_item_dto(row=row) for row in rows],
            total=rows[0].total,
        )
