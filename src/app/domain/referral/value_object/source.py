from dataclasses import dataclass
from uuid import UUID

from app.domain.common.money import Money
from app.domain.referral.enums import ReferralAwardSourceType


@dataclass(slots=True, frozen=True)
class ReferralAwardSource:
    reference_id: UUID
    type: ReferralAwardSourceType

    amount: Money
