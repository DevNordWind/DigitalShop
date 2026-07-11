from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.coupon.entity import Coupon
from app.domain.coupon.port import CouponRepository
from app.domain.coupon.value_object import CouponCode, CouponId
from app.infra.framework.sql_alchemy.table.coupon import coupon_table


class SqlACouponRepository(CouponRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, coupon: Coupon) -> None:
        self._session.add(coupon)

    @override
    async def get(self, coupon_id: CouponId) -> Coupon | None:
        stmt = select(Coupon).where(coupon_table.c.id == coupon_id)
        return await self._session.scalar(stmt)

    @override
    async def get_by_code(self, code: CouponCode) -> Coupon | None:
        stmt = select(Coupon).where(coupon_table.c.code == code)
        return await self._session.scalar(stmt)

    @override
    async def delete(self, coupon: Coupon) -> None:
        await self._session.delete(coupon)
