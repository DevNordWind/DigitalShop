from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Final

from app.common.dto.period import TimePeriod
from domain.common.money import Currency

CTX_KEY: Final[str] = "CTX_KEY"


class PeriodUnit(StrEnum):
    TODAY = "TODAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

    def calculate_from(self, now: datetime) -> datetime:
        return {
            PeriodUnit.TODAY: datetime.now(tz=UTC).replace(
                hour=0,
                minute=0,
                second=0,
            ),
            PeriodUnit.MONTH: now - timedelta(days=30),
            PeriodUnit.WEEK: now - timedelta(days=7),
        }[self]


@dataclass(slots=True)
class AdminStatisticCtx:
    convert_to: Currency

    period_unit: PeriodUnit | None = None
    custom_period: TimePeriod | None = None

    def calculate_period(self, now: datetime) -> TimePeriod | None:
        if self.custom_period is not None:
            return self.custom_period

        if self.period_unit is not None:
            return TimePeriod(
                from_date=self.period_unit.calculate_from(now), to_date=now
            )
        return None
