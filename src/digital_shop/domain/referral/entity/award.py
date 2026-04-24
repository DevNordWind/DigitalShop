from dataclasses import dataclass
from datetime import datetime

from domain.common.coefficient import Coefficient
from domain.common.exchange_rate import ExchangeRate
from domain.common.money import Money
from domain.referral.enums.status import ReferralAwardStatus
from domain.referral.value_object import ReferralAwardId, ReferralAwardSource
from domain.user.value_object import UserId


@dataclass
class ReferralAward:
    id: ReferralAwardId
    referrer_id: UserId

    status: ReferralAwardStatus

    source: ReferralAwardSource
    coefficient_snapshot: Coefficient
    award: Money | None

    exchange_rate_snapshot: ExchangeRate | None

    completed_at: datetime | None
    created_at: datetime
