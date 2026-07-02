from abc import ABC, abstractmethod

from app.domain.common.time_period import TimePeriod
from app.domain.report.report import GeneralReport


class Reporter(ABC):
    @abstractmethod
    async def report_general_by_period(
        self, period: TimePeriod | None
    ) -> GeneralReport:
        raise NotImplementedError
