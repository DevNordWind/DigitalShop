from app.common.dto.coefficient import CoefficientMapper
from app.common.dto.exchange_rate import ExchangeRateMapper
from app.common.dto.money import MoneyMapper
from app.referral.dto.award.award import ReferralAwardDTO
from app.referral.dto.source import ReferralAwardSourceMapper
from domain.referral.entity import ReferralAward


class ReferralAwardMapper:
    @classmethod
    def to_dto(cls, src: ReferralAward) -> ReferralAwardDTO:
        return ReferralAwardDTO(
            id=src.id.value,
            referrer_id=src.referrer_id.value,
            status=src.status,
            source=ReferralAwardSourceMapper.to_dto(src=src.source),
            coefficient_snapshot=CoefficientMapper.to_dto(
                src.coefficient_snapshot,
            ),
            award=MoneyMapper.to_dto(src=src.award) if src.award else None,
            exchange_rate_snapshot=ExchangeRateMapper.to_dto(
                src=src.exchange_rate_snapshot,
            )
            if src.exchange_rate_snapshot
            else None,
            completed_at=src.completed_at,
            created_at=src.created_at,
        )
