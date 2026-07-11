from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.payment.value_object import PaymentId


class PaymentIdType(TypeDecorator[PaymentId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: PaymentId | None,
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
    ) -> PaymentId | None:
        if value is None:
            return None

        return PaymentId(value=value)
