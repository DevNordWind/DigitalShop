from dataclasses import dataclass
from datetime import datetime

from app.domain.common.time_period.exception import (
    TimePeriodFromDateGreaterThanToDateError,
)


@dataclass(slots=True, frozen=True)
class TimePeriod:
    from_date: datetime
    to_date: datetime

    def __post_init__(self) -> None:
        if self.from_date > self.to_date:
            raise TimePeriodFromDateGreaterThanToDateError
