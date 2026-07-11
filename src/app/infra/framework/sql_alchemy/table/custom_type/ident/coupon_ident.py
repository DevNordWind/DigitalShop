from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.coupon.value_object import CouponId, CouponRedemptionId


class CouponRedemptionIdType(TypeDecorator[CouponRedemptionId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: CouponRedemptionId | None,
        dialect: Dialect,
    ) -> UUID | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: UUID | None,
        dialect: Dialect,
    ) -> CouponRedemptionId | None:
        if value is None:
            return None

        return CouponRedemptionId(value=value)


class CouponIdType(TypeDecorator[CouponId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: CouponId | None,
        dialect: Dialect,
    ) -> UUID | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: UUID | None,
        dialect: Dialect,
    ) -> CouponId | None:
        if value is None:
            return None

        return CouponId(value=value)
