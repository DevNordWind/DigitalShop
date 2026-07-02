from dataclasses import dataclass
from typing import Final

from app.domain.common.localized import LocalizedText
from app.domain.shopping.category.exception import (
    CategoryDescriptionTooLongError,
    CategoryDescriptionTooShortError,
)

CATEGORY_DESCRIPTION_MAX_LENGTH: Final[int] = 1024
CATEGORY_DESCRIPTION_MIN_LENGTH: Final[int] = 4


@dataclass(slots=True, frozen=True)
class CategoryDescription(LocalizedText):
    def __post_init__(self) -> None:
        super().__post_init__()

        for value in self.values.values():
            length = len(value)

            if length < CATEGORY_DESCRIPTION_MIN_LENGTH:
                raise CategoryDescriptionTooShortError(
                    min_length=CATEGORY_DESCRIPTION_MIN_LENGTH,
                )

            if length > CATEGORY_DESCRIPTION_MAX_LENGTH:
                raise CategoryDescriptionTooLongError(
                    max_length=CATEGORY_DESCRIPTION_MAX_LENGTH,
                )
