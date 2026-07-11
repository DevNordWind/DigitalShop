from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from app.app.common.dto.coefficient import CoefficientDTO
from app.app.common.dto.money import MoneyDTO
from app.domain.common.money import Currency
from app.domain.coupon.enums import CouponDiscountType


@dataclass(slots=True, frozen=True)
class FixedAmountDiscountDTO:
    type: Literal[CouponDiscountType.FIXED]
    discounts: dict[Currency, MoneyDTO]

    def get(self, currency: Currency) -> MoneyDTO | None:
        return self.discounts.get(currency)


@dataclass(slots=True, frozen=True)
class CoefficientDiscountDTO:
    type: Literal[CouponDiscountType.COEFFICIENT]
    coefficient: CoefficientDTO

    @property
    def as_percent(self) -> Decimal:
        return self.coefficient.value * Decimal("100.00")


DiscountDTO = FixedAmountDiscountDTO | CoefficientDiscountDTO
