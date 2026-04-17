from typing import Any

from app.common.dto.coefficient import CoefficientDTO
from app.common.dto.money import MoneyDTO
from app.referral.dto.award import ReferralAwardDTO
from app.referral.dto.source import ReferralAwardSourceDTO


class ReferralAwardReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> ReferralAwardDTO:
        return ReferralAwardDTO(
            id=row.id,
            referrer_id=row.referrer_id,
            status=row.status,
            source=ReferralAwardSourceDTO(
                reference_id=row.source_reference_id,
                type=row.source_type,
                amount=MoneyDTO(
                    amount=row.source_amount,
                    currency=row.source_currency,
                ),
            ),
            coefficient_snapshot=CoefficientDTO(
                value=row.coefficient_snapshot,
            ),
            award=MoneyDTO(
                amount=row.award_amount,
                currency=row.award_currency,
            )
            if row.award_amount
            else None,
            exchange_rate_snapshot=row.exchange_rate_snapshot,
            completed_at=row.completed_at,
            created_at=row.created_at,
        )
