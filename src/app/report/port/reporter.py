from abc import ABC, abstractmethod

from app.common.dto.period import TimePeriod
from app.report.dto.general_report import GeneralReport


class Reporter(ABC):
    @abstractmethod
    async def report_general_by_period(
        self, period: TimePeriod | None
    ) -> GeneralReport:
        raise NotImplementedError
