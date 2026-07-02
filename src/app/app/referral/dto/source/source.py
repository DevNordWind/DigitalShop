from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.money import MoneyDTO
from app.domain.referral.enums import ReferralAwardSourceType


@dataclass(slots=True, frozen=True)
class ReferralAwardSourceDTO:
    reference_id: UUID
    type: ReferralAwardSourceType

    amount: MoneyDTO
