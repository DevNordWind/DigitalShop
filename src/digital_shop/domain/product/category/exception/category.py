from dataclasses import dataclass

from domain.common.exception import DomainError
from domain.common.localized import Language


class CategoryError(DomainError): ...


class CategoryAccessDenied(CategoryError): ...


@dataclass
class CategoryNameAlreadyTaken(CategoryError):
    lang: Language


class CategoryDescriptionEmpty(CategoryError): ...


class CategoryArchived(CategoryError): ...


class CategoryDeletionForbidden(CategoryError): ...
