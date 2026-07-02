from datetime import datetime, timedelta
from typing import override

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.order.entity import Order
from app.domain.order.enums import OrderStatus
from app.domain.order.port import OrderRepository
from app.domain.order.value_object import OrderId
from app.infra.framework.sql_alchemy.table.order import order_table


class SqlAOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, order: Order) -> None:
        self._session.add(order)

    @override
    async def get(self, order_id: OrderId) -> Order | None:
        stmt = select(Order).where(order_table.c.id == order_id)
        return await self._session.scalar(stmt)

    @override
    async def acquire(self, order_id: OrderId) -> Order | None:
        stmt = select(Order).where(order_table.c.id == order_id.value).with_for_update()
        return await self._session.scalar(stmt)

    @override
    async def get_expired(self, now: datetime, ttl_seconds: int) -> list[Order]:
        expiry_threshold = now - timedelta(seconds=ttl_seconds)

        stmt = (
            select(Order)
            .where(
                order_table.c.status.in_(
                    [OrderStatus.NEW, OrderStatus.AWAITING_PAYMENT]
                ),
                or_(
                    and_(
                        order_table.c.awaited_payment_at.is_(None),
                        order_table.c.created_at <= expiry_threshold,
                    ),
                    and_(
                        order_table.c.awaited_payment_at.is_not(None),
                        order_table.c.awaited_payment_at <= expiry_threshold,
                    ),
                ),
            )
            .with_for_update(skip_locked=True)
        )

        result = await self._session.scalars(stmt)

        return list(result)
