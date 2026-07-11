from decimal import Decimal
from typing import override

from sqlalchemy import Dialect, Numeric, TypeDecorator

from app.domain.common.coefficient import Coefficient


class CoefficientType(TypeDecorator[Coefficient]):
    impl = Numeric(precision=4, scale=3)
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: Coefficient | None,
        dialect: Dialect,
    ) -> Decimal | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: Decimal | None,
        dialect: Dialect,
    ) -> Coefficient | None:
        if value is None:
            return None

        return Coefficient(value=value)
