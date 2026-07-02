from datetime import datetime

from app.domain.common.port import Clock, UUIDProvider
from app.domain.coupon.entity.redemption import CouponRedemption
from app.domain.coupon.enums import CouponRedemptionStatus
from app.domain.coupon.value_object import CouponId, CouponRedemptionId
from app.domain.order.value_object import OrderId
from app.domain.user.value_object import UserId


class CouponRedemptionDomainService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        coupon_id: CouponId,
        user_id: UserId,
        order_id: OrderId,
        now: datetime | None = None,
    ) -> CouponRedemption:
        actual_now: datetime = now or self._clock.now()

        return CouponRedemption(
            id=CouponRedemptionId(value=self._uuid()),
            coupon_id=coupon_id,
            user_id=user_id,
            order_id=order_id,
            status=CouponRedemptionStatus.RESERVED,
            reserved_at=actual_now,
            confirmed_at=None,
            cancelled_at=None,
        )
