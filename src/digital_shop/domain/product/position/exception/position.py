from dataclasses import dataclass

from domain.common.exception import DomainError
from domain.common.localized import Language


class PositionError(DomainError): ...


class PositionPermissionDenied(PositionError): ...


class PositionWarehouseFull(PositionError): ...


class PositionDescriptionEmpty(PositionError): ...


class PositionArchived(PositionError): ...


class InvalidItemAmount(PositionError): ...


@dataclass
class PositionNameAlreadyTaken(PositionError):
    lang: Language


@dataclass
class PositionMediaLimitReached(PositionError):
    limit: int


@dataclass
class OutOfStock(PositionError):
    available: int


class PositionDeletionForbidden(PositionError): ...
