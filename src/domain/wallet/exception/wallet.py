from dataclasses import dataclass
from decimal import Decimal

from domain.common.exception import DomainError
from domain.common.money import Currency


class WalletError(DomainError): ...


@dataclass
class WalletCurrencyMismatchError(WalletError):
    expected: Currency
    actual: Currency


class WalletPermissionDenied(WalletError): ...


@dataclass
class InsufficientFunds(WalletError):
    available_balance: Decimal
    currency: Currency
