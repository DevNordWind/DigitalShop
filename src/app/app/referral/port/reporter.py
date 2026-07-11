from abc import ABC, abstractmethod

from app.app.referral.dto.report import ReferrerReport
from app.domain.common.time_period import TimePeriod
from app.domain.user.value_object import UserId


class ReferralSystemReporter(ABC):
    @abstractmethod
    async def get_referrer_report(
        self,
        referrer_id: UserId,
        period: TimePeriod | None,
    ) -> ReferrerReport:
        raise NotImplementedError
