from sqlalchemy import Dialect, String, TypeDecorator

from domain.payment.value_object import PaymentExternalId


class PaymentExternalIdType(TypeDecorator[PaymentExternalId]):
    impl = String
    cache_ok = True

    def process_bind_param(
        self,
        value: PaymentExternalId | None,
        dialect: Dialect,
    ) -> str | None:
        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value: str | None,
        dialect: Dialect,
    ) -> PaymentExternalId | None:
        if value is None:
            return None

        return PaymentExternalId(value=value)
