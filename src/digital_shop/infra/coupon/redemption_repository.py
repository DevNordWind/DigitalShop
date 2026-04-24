from domain.coupon.entity import CouponRedemption
from domain.coupon.port import CouponRedemptionRepository
from domain.coupon.value_object import CouponRedemptionId
from domain.order.value_object import OrderId
from infra.framework.sql_alchemy.table.coupon import coupon_redemption_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CouponRedemptionRepositoryImpl(CouponRedemptionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, redemption: CouponRedemption) -> None:
        self._session.add(redemption)

    async def get(
        self,
        redemption_id: CouponRedemptionId,
    ) -> CouponRedemption | None:
        stmt = select(CouponRedemption).where(
            coupon_redemption_table.c.id == redemption_id.value,
        )
        result = await self._session.scalar(stmt)

        return result or None

    async def get_by_order_id(
        self,
        order_id: OrderId,
    ) -> CouponRedemption | None:
        stmt = select(CouponRedemption).where(
            coupon_redemption_table.c.order_id == order_id.value,
        )
        result = await self._session.scalar(stmt)

        return result or None
