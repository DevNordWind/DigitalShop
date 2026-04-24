from datetime import datetime

from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
    ExchangeRateNotFound,
)
from domain.common.money import Money
from domain.common.port import Clock, UUIDProvider
from domain.referral.entity import ReferralAward, ReferrerProfile
from domain.referral.enums.status import ReferralAwardStatus
from domain.referral.policy import ReferralPolicy
from domain.referral.value_object import ReferralAwardId, ReferralAwardSource


class ReferralAwardService:
    def __init__(
        self,
        clock: Clock,
        uuid_provider: UUIDProvider,
        rate_gateway: ExchangeRateGateway,
    ):
        self._clock: Clock = clock
        self._uuid: UUIDProvider = uuid_provider
        self._rate_gateway: ExchangeRateGateway = rate_gateway

    async def create(
        self,
        profile: ReferrerProfile,
        total: Money,
        source: ReferralAwardSource,
        policy: ReferralPolicy,
    ) -> ReferralAward:
        award_id = ReferralAwardId(self._uuid())
        now = self._clock.now()
        rate: ExchangeRate | None = None
        award: Money | None = None
        status = ReferralAwardStatus.COMPLETED
        completed_at: datetime | None = now

        if profile.award_currency != total.currency:
            try:
                rate = await self._rate_gateway.get(
                    pair=CurrencyPair(
                        source=total.currency,
                        target=profile.award_currency,
                    ),
                )
                award = policy.calculate_award(total=rate.convert(total))
            except ExchangeRateNotFound:
                status = ReferralAwardStatus.PENDING
                completed_at = None
        else:
            award = policy.calculate_award(total)

        return ReferralAward(
            id=award_id,
            referrer_id=profile.user_id,
            source=source,
            coefficient_snapshot=policy.coefficient,
            award=award,
            exchange_rate_snapshot=rate,
            completed_at=completed_at,
            created_at=now,
            status=status,
        )
