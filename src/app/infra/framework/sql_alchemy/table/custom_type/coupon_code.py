from typing import override

from sqlalchemy import Dialect, String, TypeDecorator

from app.domain.coupon.value_object import CouponCode


class CouponCodeType(TypeDecorator[CouponCode]):
    impl = String(length=64)
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: CouponCode | None,
        dialect: Dialect,
    ) -> str | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: str | None,
        dialect: Dialect,
    ) -> CouponCode | None:
        if value is None:
            return None

        return CouponCode(value=value)
