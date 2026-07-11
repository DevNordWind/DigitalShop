from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, override
from uuid import UUID

from sqlalchemy import Column, Table, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingOrder,
)
from app.app.shopping.position.dto.item import ItemDTO, ItemStatus
from app.app.shopping.position.dto.paginated import PositionItemsPaginated
from app.app.shopping.position.port import PositionItemReader
from app.domain.shopping.position.enums import FulfillmentType
from app.domain.shopping.position.item.enums import FixedItemStatus, StockItemStatus
from app.domain.shopping.position.item.value_object import FixedItemId, StockItemId
from app.domain.shopping.position.value_object import PositionId
from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)
from app.infra.shopping.position.reader.item.mapper import PositionItemMapper
from app.infra.shopping.position.reader.select import (
    FIXED_ITEM_SELECT,
    STOCK_ITEM_SELECT,
)


@dataclass(frozen=True, slots=True)
class _FulfillmentConfig:
    table: Table
    select_columns: tuple[Column[Any], ...]
    status_enum: type[FixedItemStatus] | type[StockItemStatus]
    to_dto: Callable[[Any], ItemDTO]


_FULFILLMENT_CONFIG: dict[FulfillmentType, _FulfillmentConfig] = {
    FulfillmentType.FIXED: _FulfillmentConfig(
        table=fixed_item_table,
        select_columns=FIXED_ITEM_SELECT,
        status_enum=FixedItemStatus,
        to_dto=PositionItemMapper.to_fixed_item_dto,
    ),
    FulfillmentType.STOCK: _FulfillmentConfig(
        table=stock_item_table,
        select_columns=STOCK_ITEM_SELECT,
        status_enum=StockItemStatus,
        to_dto=PositionItemMapper.to_stock_item_dto,
    ),
}


class SqlAPositionItemReader(PositionItemReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read(self, item_id: UUID) -> ItemDTO | None:
        stmt = select(*FIXED_ITEM_SELECT).where(
            fixed_item_table.c.id == FixedItemId(item_id)
        )
        row = (await self._session.execute(stmt)).first()
        if row:
            return PositionItemMapper.to_fixed_item_dto(row=row)

        stmt = select(*STOCK_ITEM_SELECT).where(
            stock_item_table.c.id == StockItemId(item_id)
        )
        row = (await self._session.execute(stmt)).first()
        if row:
            return PositionItemMapper.to_stock_item_dto(row=row)

        return None

    @override
    async def read_by_position_id(
        self,
        position_id: PositionId,
        sorting_order: SortingOrder,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        fulfillment_type: FulfillmentType | None = await self._session.scalar(
            select(position_table.c.fulfillment_type).where(
                position_table.c.id == position_id
            )
        )
        if fulfillment_type is None:
            return PositionItemsPaginated(items=[], total=0)

        config = _FULFILLMENT_CONFIG[fulfillment_type]

        order_by = self._resolve_order_by(config.table, sorting_order)

        stmt = select(
            *config.select_columns,
            func.count().over().label("total"),
        ).where(config.table.c.position_id == position_id)

        if status is not None:
            resolved_status = self._try_resolve_status(config.status_enum, status)
            if resolved_status is None:
                return PositionItemsPaginated(items=[], total=0)
            stmt = stmt.where(config.table.c.status == resolved_status)

        stmt = stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)

        rows = (await self._session.execute(stmt)).all()
        if not rows:
            return PositionItemsPaginated(items=[], total=0)

        return PositionItemsPaginated(
            items=[config.to_dto(row) for row in rows],
            total=rows[0].total,
        )

    @staticmethod
    def _resolve_order_by(table: Table, sorting_order: SortingOrder) -> Any:
        sorting_col = table.c.id

        return (
            sorting_col.asc()
            if sorting_order == SortingOrder.ASC
            else sorting_col.desc()
        )

    @staticmethod
    def _try_resolve_status(
        status_enum: type[FixedItemStatus] | type[StockItemStatus],
        status: ItemStatus,
    ) -> FixedItemStatus | StockItemStatus | None:
        try:
            return status_enum(status.value)
        except ValueError:
            return None
