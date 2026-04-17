from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Final

from domain.common.money.enums import Currency
from domain.common.money.exception import (
    CurrencyDifferenceError,
    NegativeMoneyAmount,
)

MIN_VALUE: Final[Decimal] = Decimal("0.00")
PRECISION_EXPONENT: Final[Decimal] = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        if self.amount < MIN_VALUE:
            raise NegativeMoneyAmount
        normalized: Decimal = self.amount.quantize(
            PRECISION_EXPONENT,
            rounding=ROUND_HALF_EVEN,
        )
        object.__setattr__(self, "amount", normalized)

    def __add__(self, other: Money) -> Money:
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._ensure_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: Decimal | int) -> Money:
        if isinstance(other, int):
            other = Decimal(other)
        elif not isinstance(other, Decimal):
            return NotImplemented
        return Money(amount=self.amount * other, currency=self.currency)

    def __rmul__(self, other: Decimal | int) -> Money:
        return self.__mul__(other)

    def __truediv__(self, other: Decimal | int) -> Money:
        if isinstance(other, int):
            other = Decimal(other)
        elif not isinstance(other, Decimal):
            return NotImplemented
        return Money(amount=self.amount / other, currency=self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._ensure_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._ensure_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._ensure_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._ensure_same_currency(other)
        return self.amount >= other.amount

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    @classmethod
    def zero(cls, currency: Currency) -> Money:
        return cls(currency=currency, amount=MIN_VALUE)

    def _ensure_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise CurrencyDifferenceError
