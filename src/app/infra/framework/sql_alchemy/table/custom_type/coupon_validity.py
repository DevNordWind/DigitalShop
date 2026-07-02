from datetime import datetime
from typing import override

from sqlalchemy import DateTime, Dialect, TypeDecorator

from app.domain.coupon.value_object import CouponValidity


class CouponValidityType(TypeDecorator[CouponValidity]):
    impl = DateTime(timezone=True)
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: CouponValidity | None,
        dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: datetime | None,
        dialect: Dialect,
    ) -> CouponValidity | None:
        if value is None:
            return None

        return CouponValidity(value=value)
