from collections.abc import Sequence
from typing import Protocol

from domain.common.money import Currency
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.value_object import WalletId


class WalletRepository(Protocol):
    async def add_many(self, wallets: Sequence[Wallet]) -> None:
        raise NotImplementedError

    async def get(self, wallet_id: WalletId) -> Wallet | None:
        raise NotImplementedError

    async def get_by_currency_for_update(
        self,
        user_id: UserId,
        currency: Currency,
    ) -> Wallet | None:
        raise NotImplementedError
