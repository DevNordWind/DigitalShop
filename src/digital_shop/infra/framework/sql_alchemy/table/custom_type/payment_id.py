from uuid import UUID

from domain.payment.value_object import PaymentId
from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator


class PaymentIdType(TypeDecorator[PaymentId]):
    impl = SaUUID
    cache_ok = True

    def process_bind_param(
        self,
        value: PaymentId | None,
        dialect: Dialect,
    ) -> UUID | None:
        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value: UUID | None,
        dialect: Dialect,
    ) -> PaymentId | None:
        if value is None:
            return None

        return PaymentId(value=value)
