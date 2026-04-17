from dataclasses import dataclass
from typing import Final

from domain.common.localized import LocalizedText
from domain.product.category.exception import (
    CategoryNameTooLong,
    CategoryNameTooShort,
)

CATEGORY_NAME_MAX_LENGTH: Final[int] = 64
CATEGORY_NAME_MIN_LENGTH: Final[int] = 2


@dataclass(slots=True, frozen=True)
class CategoryName(LocalizedText):
    def __post_init__(self) -> None:
        super().__post_init__()

        for value in self.values.values():
            length = len(value)

            if length < CATEGORY_NAME_MIN_LENGTH:
                raise CategoryNameTooShort(min_length=CATEGORY_NAME_MIN_LENGTH)

            if length > CATEGORY_NAME_MAX_LENGTH:
                raise CategoryNameTooLong(max_length=CATEGORY_NAME_MAX_LENGTH)
