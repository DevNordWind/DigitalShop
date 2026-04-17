from dataclasses import dataclass
from typing import Final

from domain.common.localized import LocalizedText
from domain.product.position.exception import (
    PositionNameTooLong,
    PositionNameTooShort,
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
                raise PositionNameTooShort(min_length=POSITION_NAME_MIN_LENGTH)

            if length > POSITION_NAME_MAX_LENGTH:
                raise PositionNameTooLong(max_length=POSITION_NAME_MAX_LENGTH)
