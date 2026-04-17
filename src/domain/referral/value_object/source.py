from dataclasses import dataclass
from uuid import UUID

from domain.common.money import Money
from domain.referral.enums import ReferralAwardSourceType


@dataclass(slots=True, frozen=True)
class ReferralAwardSource:
    reference_id: UUID
    type: ReferralAwardSourceType

    amount: Money
