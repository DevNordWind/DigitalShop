from dataclasses import dataclass

from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
)
from app.domain.common.localized import Language


class CategoryError(DomainError): ...


class CategoryNotFoundError(DomainError): ...


class CategoryPermissionDeniedError(CategoryError, DomainPermissionDeniedError): ...


class CategoryAlreadyArchivedError(CategoryError, DomainConflictError): ...


class CategoryAlreadyRecoveredError(CategoryError, DomainConflictError): ...


@dataclass
class CategoryNameAlreadyTakenError(CategoryError, DomainConflictError):
    lang: Language


class CategoryDescriptionEmptyError(CategoryError, DomainRuleViolationError): ...


class CategoryChangingForbiddenError(CategoryError, DomainRuleViolationError): ...


class CategoryArchivedError(CategoryChangingForbiddenError): ...


class CategoryDeletionForbiddenError(CategoryError, DomainRuleViolationError): ...
