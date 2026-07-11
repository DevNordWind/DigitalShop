from dataclasses import dataclass
from decimal import Decimal

from app.domain.common.exception import ValueObjectError


class CoefficientError(ValueObjectError): ...


@dataclass
class CoefficientTooSmallError(CoefficientError):
    min_coefficient: Decimal

    @property
    def as_percent(self) -> Decimal:
        return self.min_coefficient * Decimal("100.00")


@dataclass
class CoefficientTooBigError(CoefficientError):
    max_coefficient: Decimal

    @property
    def as_percent(self) -> Decimal:
        return self.max_coefficient * Decimal("100.00")
