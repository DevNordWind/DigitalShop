from typing import Protocol

from domain.coupon.entity import Coupon
from domain.coupon.value_object import CouponCode, CouponId


class CouponRepository(Protocol):
    async def add(self, coupon: Coupon) -> None:
        raise NotImplementedError

    async def get(self, coupon_id: CouponId) -> Coupon | None:
        raise NotImplementedError

    async def get_by_code(self, code: CouponCode) -> Coupon | None:
        raise NotImplementedError

    async def delete(self, coupon: Coupon) -> None:
        raise NotImplementedError
