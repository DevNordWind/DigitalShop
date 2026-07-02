from dataclasses import dataclass
from typing import Final

from app.domain.common.localized import LocalizedText
from app.domain.shopping.position.exception import (
    PositionDescriptionTooLongError,
    PositionDescriptionTooShortError,
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
                raise PositionDescriptionTooShortError(
                    min_length=POSITION_DESCRIPTION_MIN_LENGTH,
                )

            if length > POSITION_DESCRIPTION_MAX_LENGTH:
                raise PositionDescriptionTooLongError(
                    max_length=POSITION_DESCRIPTION_MAX_LENGTH,
                )
