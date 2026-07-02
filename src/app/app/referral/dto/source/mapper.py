from app.app.common.dto.money import MoneyMapper
from app.app.referral.dto.source.source import ReferralAwardSourceDTO
from app.domain.referral.value_object import ReferralAwardSource


class ReferralAwardSourceMapper:
    @classmethod
    def to_dto(cls, src: ReferralAwardSource) -> ReferralAwardSourceDTO:
        return ReferralAwardSourceDTO(
            reference_id=src.reference_id,
            type=src.type,
            amount=MoneyMapper.to_dto(src=src.amount),
        )

    @classmethod
    def to_value_object(
        cls,
        src: ReferralAwardSourceDTO,
    ) -> ReferralAwardSource:
        return ReferralAwardSource(
            reference_id=src.reference_id,
            type=src.type,
            amount=MoneyMapper.to_value_object(src=src.amount),
        )
