from datetime import datetime
from typing import NamedTuple

from app.domain.common.money import Currency, Money
from app.domain.common.port import Clock, UUIDProvider
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.domain.wallet.entity import Wallet
from app.domain.wallet.value_object import WalletId


class RegisteredUser(NamedTuple):
    user: User
    wallets: list[Wallet]


class UserDomainService:
    def __init__(self, clock: Clock, uuid: UUIDProvider):
        self._clock: Clock = clock
        self._uuid: UUIDProvider = uuid

    def register(
        self,
        role: UserRole,
        referrer_id: UserId | None,
    ) -> RegisteredUser:
        now: datetime = self._clock.now()
        user_id: UserId = UserId(value=self._uuid())

        wallets: list[Wallet] = [
            Wallet(
                id=WalletId(self._uuid()),
                user_id=user_id,
                balance=Money.zero(currency=currency),
            )
            for currency in Currency
        ]

        user = User(
            id=user_id,
            referrer_id=referrer_id,
            role=role,
            reg_at=now,
        )
        return RegisteredUser(user, wallets)
