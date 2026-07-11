from typing import override

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.order.dto.order import OrderDTO
from app.app.order.dto.paginated import OrdersPaginatedByReader
from app.app.order.dto.sorting import OrderSortingParams
from app.app.order.port import OrderReader
from app.domain.order.enums import OrderStatus
from app.domain.order.value_object import OrderId
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.coupon import coupon_table
from app.infra.framework.sql_alchemy.table.order import order_table
from app.infra.framework.sql_alchemy.table.payment import payment_table
from app.infra.order.reader.mapper import OrderReaderMapper
from app.infra.order.reader.select import ORDER_SELECT


class SqlAOrderReader(OrderReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def read_by_id(self, order_id: OrderId) -> OrderDTO | None:
        stmt = (
            select(*ORDER_SELECT)
            .where(order_table.c.id == order_id)
            .outerjoin(
                coupon_table,
                coupon_table.c.id == order_table.c.applied_coupon_id,
            )
            .outerjoin(
                payment_table,
                payment_table.c.purpose_reference_id == order_table.c.id,
            )
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return OrderReaderMapper.to_dto(row=row)

    @override
    async def read_by_customer_id(
        self,
        customer_id: UserId,
        sorting: OrderSortingParams,
        pagination: OffsetPaginationParams,
        status: OrderStatus | None,
    ) -> OrdersPaginatedByReader:
        sorting_col = order_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = (
            select(
                *ORDER_SELECT,
                func.count().over().label("total"),
            )
            .where(order_table.c.customer_id == customer_id)
            .outerjoin(
                coupon_table,
                coupon_table.c.id == order_table.c.applied_coupon_id,
            )
            .outerjoin(
                payment_table,
                payment_table.c.purpose_reference_id == order_table.c.id,
            )
        )
        if status is not None:
            stmt = stmt.where(order_table.c.status == status)

        stmt = stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)
        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return OrdersPaginatedByReader(orders=[], total=0)

        total = rows[0].total

        return OrdersPaginatedByReader(
            orders=[OrderReaderMapper.to_dto(row) for row in rows],
            total=total,
        )
