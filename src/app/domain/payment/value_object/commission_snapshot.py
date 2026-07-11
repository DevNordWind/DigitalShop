from dataclasses import dataclass

from app.domain.common.coefficient import Coefficient
from app.domain.common.money import Money
from app.domain.payment.enums import CommissionType


@dataclass(slots=True, frozen=True)
class CommissionSnapshot:
    type: CommissionType
    amount: Money

    coefficient: Coefficient | None
