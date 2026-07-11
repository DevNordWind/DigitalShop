from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class TimePeriodDTO:
    from_date: datetime
    to_date: datetime
