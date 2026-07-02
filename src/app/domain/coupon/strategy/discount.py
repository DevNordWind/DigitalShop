from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from frozendict import frozendict

from app.domain.common.coefficient import Coefficient
from app.domain.common.money import Currency, Money
from app.domain.coupon.enums import CouponDiscountType
from app.domain.coupon.exception import CouponDiscountUnsupportedCurrencyError


@dataclass(slots=True, frozen=True)
class DiscountStrategy(ABC):
    def calculate(self, sub_total: Money) -> Money:
        discount: Money = self._calculate(sub_total=sub_total)

        return min(discount, sub_total)

    @abstractmethod
    def _calculate(self, sub_total: Money) -> Money:
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> CouponDiscountType:
        raise NotImplementedError


@dataclass(slots=True, frozen=True)
class FixedAmountDiscount(DiscountStrategy):
    discounts: frozendict[Currency, Money]

    @override
    def _calculate(self, sub_total: Money) -> Money:
        discount: Money | None = self.discounts.get(sub_total.currency)
        if discount is None:
            raise CouponDiscountUnsupportedCurrencyError

        return discount

    @property
    @override
    def type(self) -> CouponDiscountType:
        return CouponDiscountType.FIXED


@dataclass(slots=True, frozen=True)
class CoefficientDiscount(DiscountStrategy):
    coefficient: Coefficient

    @override
    def _calculate(self, sub_total: Money) -> Money:
        return Money(
            amount=sub_total.amount * self.coefficient.value,
            currency=sub_total.currency,
        )

    @property
    @override
    def type(self) -> CouponDiscountType:
        return CouponDiscountType.COEFFICIENT
