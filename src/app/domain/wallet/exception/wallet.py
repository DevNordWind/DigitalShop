from dataclasses import dataclass

from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
    EntityNotFoundError,
)
from app.domain.common.money import Money


class WalletError(DomainError): ...


class WalletNotFoundError(WalletError, EntityNotFoundError): ...


class WalletPermissionDeniedError(WalletError, DomainPermissionDeniedError): ...


@dataclass
class InsufficientFundsError(WalletError, DomainRuleViolationError):
    available: Money
