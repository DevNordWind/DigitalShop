from dataclasses import dataclass
from datetime import datetime

from app.common.dto.period.exception import TimePeriodError


@dataclass(slots=True, frozen=True)
class TimePeriod:
    from_date: datetime
    to_date: datetime

    def __post_init__(self) -> None:
        if self.from_date > self.to_date:
            raise TimePeriodError("from_date must be <= to_date")
