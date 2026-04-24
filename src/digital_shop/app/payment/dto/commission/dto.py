from dataclasses import dataclass

from app.common.dto.coefficient import CoefficientDTO
from app.common.dto.money import MoneyDTO
from domain.payment.enums import CommissionType


@dataclass(slots=True, frozen=True)
class CommissionSnapshotDTO:
    type: CommissionType
    amount: MoneyDTO

    coefficient: CoefficientDTO | None


@dataclass(slots=True, frozen=True)
class CommissionDTO:
    type: CommissionType
    coefficient: CoefficientDTO | None
