from app.domain.common.exception import ValueObjectError


class TimePeriodError(ValueObjectError): ...


class TimePeriodFromDateGreaterThanToDateError(TimePeriodError): ...
