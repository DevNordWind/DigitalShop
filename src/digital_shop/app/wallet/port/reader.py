from abc import ABC, abstractmethod

from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from domain.user.value_object import UserId


class WalletReader(ABC):
    @abstractmethod
    async def read_by_user_id(
        self,
        user_id: UserId,
        sorting: WalletSortingParams,
    ) -> list[WalletDTO]:
        raise NotImplementedError
