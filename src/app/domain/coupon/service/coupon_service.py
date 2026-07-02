from datetime import datetime

from app.domain.common.port import Clock, UUIDProvider
from app.domain.coupon.entity import Coupon
from app.domain.coupon.strategy import DiscountStrategy
from app.domain.coupon.value_object import CouponCode, CouponId, CouponValidity
from app.domain.user.value_object import UserId


class CouponDomainService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        creator_id: UserId,
        code: CouponCode,
        discount: DiscountStrategy,
        valid_from: datetime | None = None,
        valid_until: datetime | None = None,
    ) -> Coupon:
        now: datetime = self._clock.now()

        validity_from: CouponValidity = CouponValidity.create(
            now=now, value=now if valid_from is None else valid_from
        )

        validity_until: CouponValidity | None = None

        if valid_until is not None:
            validity_until = CouponValidity.create(now=now, value=valid_until)

        return Coupon(
            id=CouponId(self._uuid()),
            creator_id=creator_id,
            code=code,
            discount=discount,
            valid_from=validity_from,
            valid_until=validity_until,
            created_at=now,
        )
