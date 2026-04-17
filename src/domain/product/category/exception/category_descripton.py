from dataclasses import dataclass

from domain.common.exception import ValueObjectError


class CategoryDescriptionError(ValueObjectError): ...


@dataclass
class CategoryDescriptionTooShort(CategoryDescriptionError):
    min_length: int


@dataclass
class CategoryDescriptionTooLong(CategoryDescriptionError):
    max_length: int
