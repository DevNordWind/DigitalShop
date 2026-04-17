from dataclasses import dataclass

from domain.common.money import Currency, Money, NegativeMoneyAmount
from domain.user.value_object import UserId
from domain.wallet.exception import (
    InsufficientFunds,
    WalletCurrencyMismatchError,
)
from domain.wallet.value_object import WalletId


@dataclass
class Wallet:
    id: WalletId
    user_id: UserId

    currency: Currency
    balance: Money

    def __post_init__(self) -> None:
        expected: Currency = self.currency
        actual: Currency = self.balance.currency

        if expected != actual:
            raise WalletCurrencyMismatchError(expected=expected, actual=actual)

    def top_up(self, amount: Money) -> None:
        self.balance = self.balance + amount

    def withdraw(self, amount: Money) -> None:
        try:
            self.balance = self.balance - amount
        except NegativeMoneyAmount as e:
            raise InsufficientFunds(
                available_balance=self.balance.amount,
                currency=self.balance.currency,
            ) from e

    def ensure_can_top_up(self, amount: Money) -> None:
        self.balance + amount
