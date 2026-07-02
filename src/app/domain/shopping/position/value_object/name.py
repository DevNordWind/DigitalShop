from dataclasses import dataclass
from typing import Final

from app.domain.common.localized import LocalizedText
from app.domain.shopping.position.exception import (
    PositionNameTooLongError,
    PositionNameTooShortError,
)

POSITION_NAME_MAX_LENGTH: Final[int] = 64
POSITION_NAME_MIN_LENGTH: Final[int] = 2


@dataclass(slots=True, frozen=True)
class PositionName(LocalizedText):
    def __post_init__(self) -> None:
        super().__post_init__()

        for value in self.values.values():
            length: int = len(value)

            if length < POSITION_NAME_MIN_LENGTH:
                raise PositionNameTooShortError(min_length=POSITION_NAME_MIN_LENGTH)

            if length > POSITION_NAME_MAX_LENGTH:
                raise PositionNameTooLongError(max_length=POSITION_NAME_MAX_LENGTH)
