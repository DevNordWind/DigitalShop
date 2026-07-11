from app.domain.common.money import Currency
from app.domain.common.port import Clock
from app.domain.referral.entity import ReferrerProfile
from app.domain.user.value_object import UserId


class ReferrerProfileDomainService:
    def __init__(self, clock: Clock):
        self._clock: Clock = clock

    def create(
        self,
        user_id: UserId,
        award_currency: Currency,
        send_notifications: bool = True,
    ) -> ReferrerProfile:

        return ReferrerProfile(
            user_id=user_id,
            award_currency=award_currency,
            send_notifications=send_notifications,
            created_at=self._clock.now(),
        )
