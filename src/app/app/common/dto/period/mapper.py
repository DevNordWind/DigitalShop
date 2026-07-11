from app.app.common.dto.period.period import TimePeriodDTO
from app.domain.common.time_period import TimePeriod


class TimePeriodMapper:
    @classmethod
    def to_value_object(cls, src: TimePeriodDTO) -> TimePeriod:
        return TimePeriod(from_date=src.from_date, to_date=src.to_date)

    @classmethod
    def to_dto(cls, src: TimePeriod) -> TimePeriodDTO:
        return TimePeriodDTO(from_date=src.from_date, to_date=src.to_date)
