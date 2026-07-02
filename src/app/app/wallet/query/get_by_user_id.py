from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.wallet.dto import WalletDTO, WalletSortingParams
from app.app.wallet.port import WalletReader
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class GetWalletsByUserIdQuery:
    target_user_id: UUID
    sorting: WalletSortingParams


class GetWalletsByUserId:
    def __init__(self, actor_provider: ActorProvider, reader: WalletReader):
        self._actor_provider = actor_provider
        self._reader: WalletReader = reader

    async def __call__(self, query: GetWalletsByUserIdQuery) -> list[WalletDTO]:
        target_user_id = UserId(query.target_user_id)

        WalletAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), target_user_id=target_user_id
        )

        wallets: list[WalletDTO] = await self._reader.read_by_user_id(
            user_id=target_user_id, sorting=query.sorting
        )
        if not wallets:
            raise UserNotFoundError

        return wallets
