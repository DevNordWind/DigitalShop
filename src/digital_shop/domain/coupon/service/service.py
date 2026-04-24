from datetime import datetime

from domain.common.port import Clock, UUIDProvider
from domain.coupon.entity import Coupon
from domain.coupon.exception import (
    CouponPermissionDenied,
)
from domain.coupon.service.access_service import CouponAccessService
from domain.coupon.strategy import DiscountStrategy
from domain.coupon.value_object import CouponCode, CouponId, CouponValidity
from domain.user.entity import User


class CouponService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        creator: User,
        code: CouponCode,
        discount: DiscountStrategy,
        valid_from: datetime | None = None,
        valid_until: datetime | None = None,
    ) -> Coupon:
        if not CouponAccessService.can_create(creator_role=creator.role):
            raise CouponPermissionDenied

        now: datetime = self._clock.now()

        validity_from: CouponValidity = CouponValidity.create(
            now=now,
            value=now,
        )
        if valid_from is not None:
            validity_from = CouponValidity.create(now=now, value=valid_from)

        validity_until: CouponValidity | None = None

        if valid_until is not None:
            validity_until = CouponValidity.create(now=now, value=valid_until)

        return Coupon(
            id=CouponId(self._uuid()),
            creator_id=creator.id,
            code=code,
            discount=discount,
            valid_from=validity_from,
            valid_until=validity_until,
            created_at=now,
        )
