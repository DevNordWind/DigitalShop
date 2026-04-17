from dataclasses import dataclass

from domain.common.coefficient import Coefficient
from domain.common.money import Money


@dataclass
class ReferralPolicy:
    coefficient: Coefficient

    def calculate_award(self, total: Money) -> Money:
        return Money(
            currency=total.currency,
            amount=total.amount * self.coefficient.value,
        )

    def change_coefficient(self, new_coefficient: Coefficient) -> None:
        self.coefficient = new_coefficient
