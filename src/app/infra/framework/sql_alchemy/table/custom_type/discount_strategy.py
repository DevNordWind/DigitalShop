from decimal import Decimal, InvalidOperation
from typing import Any, override

from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.common.coefficient import Coefficient
from app.domain.common.money import Currency, Money
from app.domain.coupon.enums import CouponDiscountType
from app.domain.coupon.strategy import (
    CoefficientDiscount,
    DiscountStrategy,
    FixedAmountDiscount,
)


class DiscountStrategyType(TypeDecorator[DiscountStrategy]):
    impl = JSONB
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: DiscountStrategy | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        match value:
            case FixedAmountDiscount():
                return {
                    "type": value.type.value,
                    "discounts": {
                        currency.value: {
                            "amount": str(amount.amount),
                            "currency": amount.currency.value,
                        }
                        for currency, amount in value.discounts.items()
                    },
                }
            case CoefficientDiscount():
                return {
                    "type": value.type.value,
                    "coefficient": str(value.coefficient.value),
                }
            case _:
                raise TypeError(
                    f"Unsupported DiscountStrategy: {type(value).__name__}",
                )

    @override
    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> DiscountStrategy | None:
        if value is None:
            return None

        try:
            coupon_type = CouponDiscountType(value["type"])
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Unknown discount type: {value.get('type')}",
            ) from e

        match coupon_type:
            case CouponDiscountType.FIXED:
                try:
                    return self._deserialize_fixed(value=value)
                except (KeyError, ValueError, InvalidOperation) as e:
                    raise ValueError(
                        f"Failed to deserialize FixedAmountDiscount: {e}",
                    ) from e

            case CouponDiscountType.COEFFICIENT:
                try:
                    return CoefficientDiscount(
                        coefficient=Coefficient(Decimal(value["coefficient"])),
                    )
                except (KeyError, ValueError, InvalidOperation) as e:
                    raise ValueError(
                        f"Failed to deserialize CoefficientDiscount: {e}",
                    ) from e

    def _deserialize_fixed(self, value: dict[str, Any]) -> FixedAmountDiscount:
        discounts: dict[Currency, Money] = {}
        for raw_currency, raw_amount in value["discounts"].items():
            currency = Currency(raw_currency)
            discounts[currency] = Money(
                amount=Decimal(raw_amount["amount"]),
                currency=currency,
            )

        return FixedAmountDiscount(discounts=frozendict(discounts))
