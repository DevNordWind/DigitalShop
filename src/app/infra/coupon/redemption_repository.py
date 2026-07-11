from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.coupon.entity import CouponRedemption
from app.domain.coupon.port import CouponRedemptionRepository
from app.domain.coupon.value_object import CouponRedemptionId
from app.domain.order.value_object import OrderId
from app.infra.framework.sql_alchemy.table.coupon import coupon_redemption_table


class SqlACouponRedemptionRepository(CouponRedemptionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, redemption: CouponRedemption) -> None:
        self._session.add(redemption)

    @override
    async def get(
        self,
        redemption_id: CouponRedemptionId,
    ) -> CouponRedemption | None:
        stmt = select(CouponRedemption).where(
            coupon_redemption_table.c.id == redemption_id
        )
        return await self._session.scalar(stmt)

    @override
    async def get_by_order_id(
        self,
        order_id: OrderId,
    ) -> CouponRedemption | None:
        stmt = select(CouponRedemption).where(
            coupon_redemption_table.c.order_id == order_id,
        )
        return await self._session.scalar(stmt)
