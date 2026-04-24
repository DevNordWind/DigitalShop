from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class CoefficientDTO:
    value: Decimal

    @property
    def as_percent(self) -> Decimal:
        return (self.value * Decimal("100.00")).quantize(Decimal("0.01"))

    @classmethod
    def from_percent(cls, percent: Decimal) -> CoefficientDTO:
        return CoefficientDTO(value=percent / Decimal("100.00"))
