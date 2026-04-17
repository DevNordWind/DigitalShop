from dataclasses import dataclass
from decimal import Decimal

from domain.common.exception import ValueObjectError


class CoefficientError(ValueObjectError): ...


@dataclass
class CoefficientTooSmall(CoefficientError):
    min_coefficient: Decimal

    @property
    def as_percent(self) -> Decimal:
        return self.min_coefficient * Decimal("100.00")


@dataclass
class CoefficientTooBig(CoefficientError):
    max_coefficient: Decimal

    @property
    def as_percent(self) -> Decimal:
        return self.max_coefficient * Decimal("100.00")
