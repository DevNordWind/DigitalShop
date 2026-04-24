from datetime import datetime

from domain.common.money import Currency, Money
from domain.common.port import Clock, UUIDProvider
from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.value_object import WalletId


class UserService:
    def __init__(self, clock: Clock, uuid: UUIDProvider):
        self._clock: Clock = clock
        self._uuid: UUIDProvider = uuid

    def register(
        self,
        role: UserRole,
        referrer_id: UserId | None,
    ) -> tuple[User, list[Wallet]]:
        now: datetime = self._clock.now()
        user_id: UserId = UserId(value=self._uuid())

        wallets: list[Wallet] = [
            Wallet(
                id=WalletId(self._uuid()),
                user_id=user_id,
                currency=currency,
                balance=Money.zero(currency=currency),
            )
            for currency in Currency
        ]

        return User(
            id=user_id,
            referrer_id=referrer_id,
            role=role,
            reg_at=now,
        ), wallets
