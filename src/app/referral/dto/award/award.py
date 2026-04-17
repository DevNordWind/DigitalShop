from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.dto.coefficient import CoefficientDTO
from app.common.dto.exchange_rate import ExchangeRateDTO
from app.common.dto.money import MoneyDTO
from app.referral.dto.source import ReferralAwardSourceDTO
from domain.referral.enums.status import ReferralAwardStatus


@dataclass(slots=True, frozen=True)
class ReferralAwardDTO:
    id: UUID
    referrer_id: UUID

    status: ReferralAwardStatus

    source: ReferralAwardSourceDTO
    coefficient_snapshot: CoefficientDTO
    award: MoneyDTO | None

    exchange_rate_snapshot: ExchangeRateDTO | None

    completed_at: datetime | None
    created_at: datetime
