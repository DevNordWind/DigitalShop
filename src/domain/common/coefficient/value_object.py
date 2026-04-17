from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from domain.common.coefficient.exception import (
    CoefficientTooBig,
    CoefficientTooSmall,
)

MIN_COEFFICIENT: Final[Decimal] = Decimal("0.001")
MAX_COEFFICIENT: Final[Decimal] = Decimal("1.00")
COEFFICIENT_PRECISION: Final[Decimal] = Decimal("0.001")


@dataclass(slots=True, frozen=True)
class Coefficient:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < MIN_COEFFICIENT:
            raise CoefficientTooSmall(min_coefficient=MIN_COEFFICIENT)

        if self.value > MAX_COEFFICIENT:
            raise CoefficientTooBig(max_coefficient=MAX_COEFFICIENT)

        normalized = self.value.quantize(COEFFICIENT_PRECISION)
        object.__setattr__(self, "value", normalized)
