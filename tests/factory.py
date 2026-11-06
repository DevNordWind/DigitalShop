from polyfactory.factories import DataclassFactory

from app.domain.common.actor import SystemActor, UserActor
from app.domain.common.money import Money
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


class SystemActorFactory(DataclassFactory[SystemActor]): ...


class MoneyFactory(DataclassFactory[Money]): ...


class UserActorFactory(DataclassFactory[UserActor]):
    role = UserRole.USER


class UserFactory(DataclassFactory[User]): ...


class WalletFactory(DataclassFactory[Wallet]): ...
