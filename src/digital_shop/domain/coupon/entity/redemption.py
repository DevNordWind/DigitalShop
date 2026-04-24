from dataclasses import dataclass
from datetime import datetime

from domain.coupon.enums import CouponRedemptionStatus
from domain.coupon.exception import (
    CouponRedemptionCancellationForbidden,
    CouponRedemptionConfirmationForbidden,
)
from domain.coupon.value_object import CouponId, CouponRedemptionId
from domain.order.value_object import OrderId
from domain.user.value_object import UserId


@dataclass(kw_only=True)
class CouponRedemption:
    id: CouponRedemptionId

    coupon_id: CouponId
    user_id: UserId
    order_id: OrderId

    status: CouponRedemptionStatus = CouponRedemptionStatus.RESERVED
    reserved_at: datetime
    confirmed_at: datetime | None
    cancelled_at: datetime | None

    def confirm(self, now: datetime) -> None:
        if self.status != CouponRedemptionStatus.RESERVED:
            raise CouponRedemptionConfirmationForbidden

        self.status = CouponRedemptionStatus.CONFIRMED
        self.confirmed_at = now

    def cancel(self, now: datetime) -> None:
        if self.status != CouponRedemptionStatus.RESERVED:
            raise CouponRedemptionCancellationForbidden

        self.status = CouponRedemptionStatus.CANCELLED
        self.cancelled_at = now
