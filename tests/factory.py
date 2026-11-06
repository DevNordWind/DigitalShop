import random
from decimal import Decimal

from polyfactory.factories import DataclassFactory
from polyfactory.fields import Use

from app.domain.common.actor import SystemActor, UserActor
from app.domain.common.money import Currency, Money
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.wallet.entity import Wallet

__all__ = (
    "MoneyFactory",
    "SystemActorFactory",
    "UserActorFactory",
    "UserFactory",
    "WalletFactory",
)


def _random_money_amount(
    low: Decimal = Decimal("0.00"),
    high: Decimal = Decimal("10000.00"),
) -> Decimal:
    cents = random.randint(int(low * 100), int(high * 100))
    return Decimal(cents).scaleb(-2)


class SystemActorFactory(DataclassFactory[SystemActor]): ...


class MoneyFactory(DataclassFactory[Money]):
    currency = Currency.USD
    amount = Use(_random_money_amount)


class UserActorFactory(DataclassFactory[UserActor]):
    role = UserRole.USER


class UserFactory(DataclassFactory[User]): ...


class WalletFactory(DataclassFactory[Wallet]): ...
