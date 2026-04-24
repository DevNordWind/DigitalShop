from decimal import Decimal, InvalidOperation
from typing import Any

from domain.common.coefficient import Coefficient
from domain.common.money import Currency, Money
from domain.coupon.enums import CouponType
from domain.coupon.strategy import (
    CoefficientDiscount,
    DiscountStrategy,
    FixedAmountDiscount,
)
from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class DiscountStrategyType(TypeDecorator[DiscountStrategy]):
    impl = JSONB
    cache_ok = True

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

    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> DiscountStrategy | None:
        if value is None:
            return None

        try:
            coupon_type = CouponType(value["type"])
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Unknown discount type: {value.get('type')}",
            ) from e

        match coupon_type:
            case CouponType.FIXED:
                try:
                    return self._deserialize_fixed(value=value)
                except (KeyError, ValueError, InvalidOperation) as e:
                    raise ValueError(
                        f"Failed to deserialize FixedAmountDiscount: {e}",
                    ) from e

            case CouponType.COEFFICIENT:
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
