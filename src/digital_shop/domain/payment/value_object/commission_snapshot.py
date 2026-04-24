from dataclasses import dataclass

from domain.common.coefficient import Coefficient
from domain.common.money import Money
from domain.payment.enums import CommissionType


@dataclass(slots=True, frozen=True)
class CommissionSnapshot:
    type: CommissionType
    amount: Money

    coefficient: Coefficient | None
