from collections.abc import Sequence
from typing import Any, override
from uuid import UUID

from sqlalchemy import Column, Table, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.selectable import Select

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.shopping.position.dto.item import ItemDTO, ItemStatus
from app.app.shopping.position.dto.paginated import (
    PositionItemsPaginated,
    PositionsPaginated,
    PositionsShortPaginated,
    PositionWithItemsAmountPaginated,
)
from app.app.shopping.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionWithItemsAmount,
)
from app.app.shopping.position.dto.sorting import (
    PositionItemsSortingParams,
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
from app.infra.shopping.position.reader.mapper import PositionReaderMapper
from app.infra.shopping.position.reader.select import (
    FIXED_ITEM_SELECT,
    POSITION_SELECT,
    POSITION_SHORT_SELECT,
    STOCK_ITEM_SELECT,
)
from app.infra.shopping.position.reader.subq import ITEM_EXISTS_SUBQ, ITEMS_COUNT_SUBQ

_ITEM_TABLES: dict[FulfillmentType, Table] = {
    FulfillmentType.FIXED: fixed_item_table,
    FulfillmentType.STOCK: stock_item_table,
}

_ITEM_SELECTS: dict[FulfillmentType, tuple[Column[Any], ...]] = {
    FulfillmentType.FIXED: FIXED_ITEM_SELECT,
    FulfillmentType.STOCK: STOCK_ITEM_SELECT,
}

_ITEM_STATUS_ENUMS: dict[FulfillmentType, type] = {
    FulfillmentType.FIXED: FixedItemStatus,
    FulfillmentType.STOCK: StockItemStatus,
}


class SqlAPositionReader(PositionReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def read(self, position_id: PositionId) -> PositionDTO | None:
        stmt = select(*POSITION_SELECT).where(position_table.c.id == position_id.value)
        row = (await self._session.execute(stmt)).first()
        return PositionReaderMapper.to_dto(row=row) if row else None

    @override
    async def read_short(self, position_id: PositionId) -> PositionShortDTO | None:
        stmt = select(*POSITION_SHORT_SELECT).where(
            position_table.c.id == position_id.value
        )
        row = (await self._session.execute(stmt)).first()
        return PositionReaderMapper.to_short_dto(row=row) if row else None

    @override
    async def read_with_items_amount(
        self, position_id: PositionId
    ) -> PositionWithItemsAmount | None:
        stmt = select(*POSITION_SELECT).where(position_table.c.id == position_id.value)
        row = (await self._session.execute(stmt)).first()
        if not row:
            return None

        items_amount = await self._count_items_amount(
            fulfillment_type=row.fulfillment_type, position_id=position_id
        )
        return PositionWithItemsAmount(
            position=PositionReaderMapper.to_dto(row=row),
            items_amount=items_amount,
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
    async def read_with_items_amount_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> PositionWithItemsAmountPaginated:
        stmt = self._build_position_query(
            select_columns=(*POSITION_SELECT, ITEMS_COUNT_SUBQ),
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
    async def read_all_by_category_id(
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
    async def read_item(self, item_id: UUID) -> ItemDTO | None:
        for fulfillment_type, table in _ITEM_TABLES.items():
            select_columns = _ITEM_SELECTS[fulfillment_type]

            stmt = select(*select_columns).where(table.c.id == item_id)
            row = (await self._session.execute(stmt)).first()
            if row:
                return PositionReaderMapper.to_item_dto(
                    row=row, fulfillment_type=fulfillment_type
                )

        return None

    @override
    async def read_items(
        self,
        position_id: PositionId,
        sorting: PositionItemsSortingParams,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        fulfillment_type: FulfillmentType | None = await self._session.scalar(
            select(position_table.c.fulfillment_type).where(
                position_table.c.id == position_id.value
            )
        )
        if fulfillment_type is None:
            return PositionItemsPaginated(items=[], total=0)

        table = self._resolve_item_table(fulfillment_type)
        select_columns = _ITEM_SELECTS[fulfillment_type]

        sorting_col = table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *select_columns,
            func.count().over().label("total"),
        ).where(table.c.position_id == position_id.value)

        if status is not None:
            status_enum = _ITEM_STATUS_ENUMS[fulfillment_type]
            stmt = stmt.where(table.c.status == status_enum(status.value))

        stmt = stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)

        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionItemsPaginated(items=[], total=0)

        return PositionItemsPaginated(
            items=[
                PositionReaderMapper.to_item_dto(
                    row=row, fulfillment_type=fulfillment_type
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
        sorting_col = position_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *select_columns,
            func.count().over().label("total"),
        ).where(position_table.c.category_id == category_id.value)

        if status is not None:
            stmt = stmt.where(position_table.c.status == status)

        if show_with_no_items is False:
            stmt = stmt.where(ITEM_EXISTS_SUBQ)

        return stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)

    async def _count_items_amount(
        self, fulfillment_type: FulfillmentType, position_id: PositionId
    ) -> int:
        table = self._resolve_item_table(fulfillment_type)
        stmt = select(func.count(table.c.id)).where(
            table.c.position_id == position_id.value
        )
        return await self._session.scalar(stmt) or 0

    @staticmethod
    def _resolve_item_table(fulfillment_type: FulfillmentType) -> Table:
        try:
            return _ITEM_TABLES[fulfillment_type]
        except KeyError as e:
            raise ValueError(f"Unknown fulfillment type: {fulfillment_type}") from e
