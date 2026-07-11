from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.domain.common.money import Currency
from app.domain.user.value_object import UserId
from app.domain.wallet.entity import Wallet
from app.domain.wallet.value_object import WalletId


class WalletRepository(ABC):
    @abstractmethod
    async def add_many(self, wallets: Sequence[Wallet]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id_currency(
        self, user_id: UserId, currency: Currency
    ) -> Wallet | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self, wallet_id: WalletId) -> Wallet | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire_user_id_by_currency(
        self,
        user_id: UserId,
        currency: Currency,
    ) -> Wallet | None:
        raise NotImplementedError
