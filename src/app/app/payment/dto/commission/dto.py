from dataclasses import dataclass

from app.app.common.dto.coefficient import CoefficientDTO
from app.app.common.dto.money import MoneyDTO
from app.domain.payment.enums import CommissionType


@dataclass(slots=True, frozen=True)
class CommissionSnapshotDTO:
    type: CommissionType
    amount: MoneyDTO

    coefficient: CoefficientDTO | None


@dataclass(slots=True, frozen=True)
class CommissionDTO:
    type: CommissionType
    coefficient: CoefficientDTO | None
