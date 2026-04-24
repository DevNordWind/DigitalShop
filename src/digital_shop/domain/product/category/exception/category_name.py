from dataclasses import dataclass

from domain.common.localized import LocalizedTextError


class CategoryNameError(LocalizedTextError): ...


@dataclass
class CategoryNameTooLong(CategoryNameError):
    max_length: int


@dataclass
class CategoryNameTooShort(CategoryNameError):
    min_length: int
