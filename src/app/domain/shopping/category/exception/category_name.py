from dataclasses import dataclass

from app.domain.common.localized import LocalizedTextError


class CategoryNameError(LocalizedTextError): ...


@dataclass
class CategoryNameTooLongError(CategoryNameError):
    max_length: int


@dataclass
class CategoryNameTooShortError(CategoryNameError):
    min_length: int
