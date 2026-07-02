from dataclasses import dataclass

from app.domain.common.exception import ValueObjectError


class CategoryDescriptionError(ValueObjectError): ...


@dataclass
class CategoryDescriptionTooShortError(CategoryDescriptionError):
    min_length: int


@dataclass
class CategoryDescriptionTooLongError(CategoryDescriptionError):
    max_length: int
