from datetime import datetime

from sqlalchemy import DateTime, Dialect, TypeDecorator

from domain.coupon.value_object import CouponValidity


class CouponValidityType(TypeDecorator[CouponValidity]):
    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self,
        value: CouponValidity | None,
        dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value: datetime | None,
        dialect: Dialect,
    ) -> CouponValidity | None:
        if value is None:
            return None

        return CouponValidity(value=value)
