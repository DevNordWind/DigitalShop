from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.wallet.dto import WalletDTO, WalletSortingParams
from app.app.wallet.port import WalletReader
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class ListWalletsByUserIdQuery:
    target_user_id: UUID

    sorting: WalletSortingParams


class ListWalletsByUserId:
    def __init__(self, reader: WalletReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: ListWalletsByUserIdQuery,
    ) -> list[WalletDTO]:
        target_user_id: UserId = UserId(query.target_user_id)
        WalletAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), target_user_id=target_user_id
        )

        wallets: list[WalletDTO] = await self._reader.read_by_user_id(
            user_id=target_user_id, sorting=query.sorting
        )
        if not wallets:
            raise UserNotFoundError

        return wallets
