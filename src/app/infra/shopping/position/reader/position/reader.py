from collections.abc import Sequence
from typing import Any, override

from sqlalchemy import Table, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.selectable import Select

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.shopping.position.dto.item import ItemStatus
from app.app.shopping.position.dto.paginated import (
    PositionShortWithItemsAmountPaginated,
    PositionsPaginated,
    PositionsShortPaginated,
    PositionWithItemsAmountPaginated,
)
from app.app.shopping.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionShortWithItemsAmount,
    PositionWithItemsAmount,
)
from app.app.shopping.position.dto.sorting import (
    PositionSortingParams,
)
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.enums import FulfillmentType, PositionStatus
from app.domain.shopping.position.item.enums import (
    FixedItemStatus,
    StockItemStatus,
)
from app.domain.shopping.position.value_object import PositionId
from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)
from app.infra.shopping.position.reader.position.mapper import PositionReaderMapper
from app.infra.shopping.position.reader.select import (
    POSITION_SELECT,
    POSITION_SHORT_SELECT,
)
from app.infra.shopping.position.reader.subq import ITEM_EXISTS_SUBQ, ITEMS_COUNT_SUBQ

_ITEM_STATUS_ENUMS: dict[FulfillmentType, type] = {
    FulfillmentType.FIXED: FixedItemStatus,
    FulfillmentType.STOCK: StockItemStatus,
}


class SqlAPositionReader(PositionReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def read(self, position_id: PositionId) -> PositionDTO | None:
        stmt = select(*POSITION_SELECT).where(position_table.c.id == position_id)
        row = (await self._session.execute(stmt)).first()
        return PositionReaderMapper.to_dto(row=row) if row else None

    @override
    async def read_short(self, position_id: PositionId) -> PositionShortDTO | None:
        stmt = select(*POSITION_SHORT_SELECT).where(position_table.c.id == position_id)
        row = (await self._session.execute(stmt)).first()
        return PositionReaderMapper.to_short_dto(row=row) if row else None

    @override
    async def read_with_items_amount(
        self,
        position_id: PositionId,
        item_status: ItemStatus | None = None,
    ) -> PositionWithItemsAmount | None:
        items_amount_column = self._build_items_count_column(item_status)
        stmt = select(*POSITION_SELECT, items_amount_column).where(
            position_table.c.id == position_id
        )
        row = (await self._session.execute(stmt)).first()
        if not row:
            return None

        return PositionWithItemsAmount(
            position=PositionReaderMapper.to_dto(row=row),
            items_amount=row.items_amount,
        )

    @override
    async def read_short_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        show_with_no_items: bool | None,
        status: PositionStatus | None,
    ) -> PositionsShortPaginated:
        stmt = self._build_position_query(
            select_columns=POSITION_SHORT_SELECT,
            category_id=category_id,
            sorting=sorting,
            pagination=pagination,
            status=status,
            show_with_no_items=show_with_no_items,
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionsShortPaginated(positions=[], total=0)

        return PositionsShortPaginated(
            positions=[PositionReaderMapper.to_short_dto(row=row) for row in rows],
            total=rows[0].total,
        )

    @override
    async def read_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> PositionsPaginated:
        stmt = self._build_position_query(
            select_columns=POSITION_SELECT,
            category_id=category_id,
            sorting=sorting,
            pagination=pagination,
            status=status,
            show_with_no_items=show_with_no_items,
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionsPaginated(positions=[], total=0)

        return PositionsPaginated(
            positions=[PositionReaderMapper.to_dto(row=row) for row in rows],
            total=rows[0].total,
        )

    @override
    async def read_with_items_amount_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
        item_status: ItemStatus | None = None,
    ) -> PositionWithItemsAmountPaginated:
        items_amount_column = self._build_items_count_column(item_status)
        stmt = self._build_position_query(
            select_columns=(*POSITION_SELECT, items_amount_column),
            category_id=category_id,
            sorting=sorting,
            pagination=pagination,
            status=status,
            show_with_no_items=show_with_no_items,
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionWithItemsAmountPaginated(positions=[], total=0)

        return PositionWithItemsAmountPaginated(
            positions=[
                PositionWithItemsAmount(
                    position=PositionReaderMapper.to_dto(row=row),
                    items_amount=row.items_amount,
                )
                for row in rows
            ],
            total=rows[0].total,
        )

    @override
    async def read_short_with_items_amount_by_ids(
        self,
        position_ids: Sequence[PositionId],
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        item_status: ItemStatus | None = None,
    ) -> PositionShortWithItemsAmountPaginated:
        if not position_ids:
            return PositionShortWithItemsAmountPaginated(positions=[], total=0)

        order_by = self._resolve_order_by(sorting)
        items_amount_column = self._build_items_count_column(item_status)

        stmt = (
            select(
                *POSITION_SHORT_SELECT,
                items_amount_column,
                func.count().over().label("total"),
            )
            .where(position_table.c.id.in_(position_ids))
            .order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionShortWithItemsAmountPaginated(positions=[], total=0)

        return PositionShortWithItemsAmountPaginated(
            positions=[
                PositionShortWithItemsAmount(
                    position=PositionReaderMapper.to_short_dto(row=row),
                    items_amount=row.items_amount,
                )
                for row in rows
            ],
            total=rows[0].total,
        )

    def _build_position_query(
        self,
        select_columns: Sequence[ColumnElement[Any]],
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> Select[Any]:
        order_by = self._resolve_order_by(sorting)

        stmt = select(
            *select_columns,
            func.count().over().label("total"),
        ).where(position_table.c.category_id == category_id)

        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        if show_with_no_items is False:
            stmt = stmt.where(ITEM_EXISTS_SUBQ)

        return stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)

    @staticmethod
    def _resolve_order_by(sorting: PositionSortingParams) -> ColumnElement[Any]:
        sorting_col = position_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        return (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

    def _build_items_count_column(
        self, item_status: ItemStatus | None
    ) -> ColumnElement[Any]:
        if item_status is None:
            return ITEMS_COUNT_SUBQ

        fixed_count = self._item_count_subquery(
            FulfillmentType.FIXED, fixed_item_table, item_status
        )
        stock_count = self._item_count_subquery(
            FulfillmentType.STOCK, stock_item_table, item_status
        )
        return (fixed_count + stock_count).label("items_amount")

    def _item_count_subquery(
        self,
        fulfillment_type: FulfillmentType,
        table: Table,
        item_status: ItemStatus,
    ) -> ColumnElement[Any]:
        resolved_status = self._try_resolve_item_status(fulfillment_type, item_status)
        if resolved_status is None:
            return literal(0)

        return (
            select(func.count(table.c.id))
            .where(
                table.c.position_id == position_table.c.id,
                table.c.status == resolved_status,
            )
            .correlate(position_table)
            .scalar_subquery()
        )

    @staticmethod
    def _try_resolve_item_status(
        fulfillment_type: FulfillmentType, item_status: ItemStatus
    ) -> FixedItemStatus | StockItemStatus | None:
        status_enum = _ITEM_STATUS_ENUMS[fulfillment_type]
        try:
            return status_enum(item_status.value)
        except ValueError:
            return None
