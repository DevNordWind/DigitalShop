from abc import ABC, abstractmethod

from domain.coupon.entity import CouponRedemption
from domain.coupon.value_object import CouponRedemptionId
from domain.order.value_object import OrderId


class CouponRedemptionRepository(ABC):
    @abstractmethod
    async def add(self, redemption: CouponRedemption) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        redemption_id: CouponRedemptionId,
    ) -> CouponRedemption | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_order_id(
        self,
        order_id: OrderId,
    ) -> CouponRedemption | None:
        raise NotImplementedError
