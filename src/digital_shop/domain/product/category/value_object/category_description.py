from dataclasses import dataclass
from typing import Final

from domain.common.localized import LocalizedText
from domain.product.category.exception import (
    CategoryDescriptionTooLong,
    CategoryDescriptionTooShort,
)

CATEGORY_DESCRIPTION_MAX_LENGTH: Final[int] = 512
CATEGORY_DESCRIPTION_MIN_LENGTH: Final[int] = 4


@dataclass(slots=True, frozen=True)
class CategoryDescription(LocalizedText):
    def __post_init__(self) -> None:
        super().__post_init__()

        for value in self.values.values():
            length = len(value)

            if length < CATEGORY_DESCRIPTION_MIN_LENGTH:
                raise CategoryDescriptionTooShort(
                    min_length=CATEGORY_DESCRIPTION_MIN_LENGTH,
                )

            if length > CATEGORY_DESCRIPTION_MAX_LENGTH:
                raise CategoryDescriptionTooLong(
                    max_length=CATEGORY_DESCRIPTION_MAX_LENGTH,
                )
