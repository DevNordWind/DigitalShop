from typing import override

from sqlalchemy import Dialect, String, TypeDecorator

from app.domain.payment.value_object import PaymentExternalId


class PaymentExternalIdType(TypeDecorator[PaymentExternalId]):
    impl = String
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: PaymentExternalId | None,
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
    ) -> PaymentExternalId | None:
        if value is None:
            return None

        return PaymentExternalId(value=value)
