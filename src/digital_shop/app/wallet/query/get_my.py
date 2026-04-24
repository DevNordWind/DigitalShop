from dataclasses import dataclass

from app.user.port import UserIdentifyProvider
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from app.wallet.port import WalletReader


@dataclass(slots=True, frozen=True)
class GetMyWalletsQuery:
    sorting: WalletSortingParams


class GetMyWallets:
    def __init__(self, idp: UserIdentifyProvider, reader: WalletReader):
        self._idp: UserIdentifyProvider = idp
        self._reader: WalletReader = reader

    async def __call__(self, query: GetMyWalletsQuery) -> list[WalletDTO]:
        return await self._reader.read_by_user_id(
            user_id=await self._idp.get_user_id(),
            sorting=query.sorting,
        )
