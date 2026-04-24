from domain.common.money import Currency
from domain.common.port import Clock
from domain.referral.entity import ReferrerProfile
from domain.user.value_object import UserId


class ReferrerProfileService:
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
