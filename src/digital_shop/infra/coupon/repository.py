from domain.coupon.entity import Coupon
from domain.coupon.port import CouponRepository
from domain.coupon.value_object import CouponCode, CouponId
from infra.framework.sql_alchemy.table.coupon import coupon_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CouponRepositoryImpl(CouponRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, coupon: Coupon) -> None:
        self._session.add(coupon)

    async def get(self, coupon_id: CouponId) -> Coupon | None:
        stmt = select(Coupon).where(coupon_table.c.id == coupon_id.value)
        result = await self._session.scalar(stmt)

        return result or None

    async def get_by_code(self, code: CouponCode) -> Coupon | None:
        stmt = select(Coupon).where(coupon_table.c.code == code.value)
        result = await self._session.scalar(stmt)

        return result or None

    async def delete(self, coupon: Coupon) -> None:
        await self._session.delete(coupon)
