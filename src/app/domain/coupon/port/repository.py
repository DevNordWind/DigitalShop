from abc import ABC, abstractmethod

from app.domain.coupon.entity import Coupon
from app.domain.coupon.value_object import CouponCode, CouponId


class CouponRepository(ABC):
    @abstractmethod
    async def add(self, coupon: Coupon) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, coupon_id: CouponId) -> Coupon | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_code(self, code: CouponCode) -> Coupon | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, coupon: Coupon) -> None:
        raise NotImplementedError
