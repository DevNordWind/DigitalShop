from app.referral.dto.profile.profile import ReferrerProfileDTO
from domain.referral.entity import ReferrerProfile


class ReferrerProfileMapper:
    @classmethod
    def to_dto(cls, src: ReferrerProfile) -> ReferrerProfileDTO:
        return ReferrerProfileDTO(
            user_id=src.user_id.value,
            award_currency=src.award_currency,
            send_notifications=src.send_notifications,
        )
