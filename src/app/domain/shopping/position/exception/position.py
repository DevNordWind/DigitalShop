from dataclasses import dataclass

from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
    EntityNotFoundError,
)
from app.domain.common.localized import Language


class PositionError(DomainError): ...


class PositionPermissionDeniedError(PositionError, DomainPermissionDeniedError): ...


class PositionMediaNotFoundError(PositionError, EntityNotFoundError): ...


class PositionNotFoundError(PositionError, EntityNotFoundError): ...


class PositionAlreadyArchivedError(PositionError, DomainConflictError): ...


class PositionIncompatibleStrategyError(PositionError, DomainConflictError): ...


class PositionNotArchivedError(PositionError, DomainConflictError): ...


class PositionDescriptionEmptyError(PositionError, DomainConflictError): ...


@dataclass
class PositionNameAlreadyTakenError(PositionError, DomainConflictError):
    lang: Language


@dataclass
class PositionMediaLimitReachedError(PositionError, DomainRuleViolationError):
    limit: int


class PositionChangingForbiddenError(PositionError, DomainRuleViolationError): ...


class PositionArchivedError(PositionError, DomainRuleViolationError): ...


class PositionDeletionForbiddenError(PositionError, DomainRuleViolationError): ...


class PositionWarehouseError(PositionError): ...


class NothingToAddError(PositionWarehouseError, DomainConflictError): ...


class PositionWarehouseFullError(PositionWarehouseError, DomainRuleViolationError): ...


@dataclass
class OutOfStockError(PositionWarehouseError, DomainRuleViolationError):
    available: int


class PositionItemError(PositionError): ...


class PositionItemNotFoundError(PositionItemError, EntityNotFoundError): ...
