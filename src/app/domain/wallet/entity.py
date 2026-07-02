from dataclasses import dataclass

from app.domain.common.money import Money, NegativeMoneyAmountError
from app.domain.user.value_object import UserId
from app.domain.wallet.exception import (
    InsufficientFundsError,
)
from app.domain.wallet.value_object import WalletId


@dataclass
class Wallet:
    id: WalletId
    user_id: UserId

    balance: Money

    def top_up(self, amount: Money) -> None:
        self.balance = self.balance + amount

    def withdraw(self, amount: Money) -> None:
        try:
            self.balance = self.balance - amount
        except NegativeMoneyAmountError as e:
            raise InsufficientFundsError(available=self.balance) from e

    def ensure_can_top_up(self, amount: Money) -> None:
        self.balance + amount
