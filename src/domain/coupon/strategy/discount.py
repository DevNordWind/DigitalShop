from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from domain.common.coefficient import Coefficient
from domain.common.money import Currency, Money
from domain.coupon.enums import CouponType
from domain.coupon.exception import CouponDiscountUnsupportedCurrency


class DiscountStrategy(ABC):
    def calculate(self, sub_total: Money) -> Money:
        discount: Money = self._calculate(sub_total=sub_total)
        return min(discount, sub_total)

    @abstractmethod
    def _calculate(self, sub_total: Money) -> Money:
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> CouponType:
        raise NotImplementedError


@dataclass(slots=True, frozen=True)
class FixedAmountDiscount(DiscountStrategy):
    discounts: frozendict[Currency, Money]

    def _calculate(self, sub_total: Money) -> Money:
        discount: Money | None = self.discounts.get(sub_total.currency)
        if discount is None:
            raise CouponDiscountUnsupportedCurrency

        return discount

    @property
    def type(self) -> CouponType:
        return CouponType.FIXED


@dataclass(slots=True, frozen=True)
class CoefficientDiscount(DiscountStrategy):
    coefficient: Coefficient

    def _calculate(self, sub_total: Money) -> Money:
        return Money(
            amount=sub_total.amount * self.coefficient.value,
            currency=sub_total.currency,
        )

    @property
    def type(self) -> CouponType:
        return CouponType.COEFFICIENT
