from abc import ABC, abstractmethod

from app.common.dto.period import TimePeriod
from app.referral.dto.report import ReferrerReport
from domain.user.value_object import UserId


class ReferralSystemReporter(ABC):
    @abstractmethod
    async def get_referrer_report(
        self,
        referrer_id: UserId,
        period: TimePeriod | None,
    ) -> ReferrerReport:
        raise NotImplementedError
