from dataclasses import dataclass
from typing import Final

from app.domain.shopping.position.item.exception import (
    ItemContentTooLongError,
    ItemContentTooShortError,
)

_MIN_LENGTH: Final[int] = 1
_MAX_LENGTH: Final[int] = 1024


@dataclass(slots=True, frozen=True)
class ItemContent:
    value: str

    def __post_init__(self) -> None:
        length: int = len(self.value)

        if length < _MIN_LENGTH:
            raise ItemContentTooShortError(min_length=_MIN_LENGTH)
        if length > _MAX_LENGTH:
            raise ItemContentTooLongError(max_length=_MAX_LENGTH)
