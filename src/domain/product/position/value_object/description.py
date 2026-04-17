from dataclasses import dataclass
from typing import Final

from domain.common.localized import LocalizedText
from domain.product.position.exception import (
    PositionDescriptionTooLong,
    PositionDescriptionTooShort,
)

POSITION_DESCRIPTION_MAX_LENGTH: Final[int] = 512
POSITION_DESCRIPTION_MIN_LENGTH: Final[int] = 4


@dataclass(slots=True, frozen=True)
class PositionDescription(LocalizedText):
    def __post_init__(self) -> None:
        super().__post_init__()

        for value in self.values.values():
            length: int = len(value)

            if length < POSITION_DESCRIPTION_MIN_LENGTH:
                raise PositionDescriptionTooShort(
                    min_length=POSITION_DESCRIPTION_MIN_LENGTH,
                )

            if length > POSITION_DESCRIPTION_MAX_LENGTH:
                raise PositionDescriptionTooLong(
                    max_length=POSITION_DESCRIPTION_MAX_LENGTH,
                )
