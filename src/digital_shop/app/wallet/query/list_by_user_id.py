from dataclasses import dataclass
from uuid import UUID

from app.user.exception import UserNotFound
from app.user.service import GetCurrentUser
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from app.wallet.port import WalletReader
from domain.user.entity import User
from domain.user.port import UserRepository
from domain.user.value_object import UserId
from domain.wallet.exception import WalletPermissionDenied
from domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class ListWalletsByUserIdQuery:
    user_id: UUID
    sorting: WalletSortingParams


class ListWalletsByUserId:
    def __init__(
        self,
        reader: WalletReader,
        user_repo: UserRepository,
        current_user: GetCurrentUser,
    ):
        self._user_repo: UserRepository = user_repo
        self._current_user: GetCurrentUser = current_user
        self._reader: WalletReader = reader

    async def __call__(
        self,
        query: ListWalletsByUserIdQuery,
    ) -> list[WalletDTO]:
        viewer: User = await self._current_user()
        target_user_id: UserId = UserId(query.user_id)
        if not WalletAccessService.can_view(
            viewer=viewer, wallet_user_id=target_user_id
        ):
            raise WalletPermissionDenied

        wallets: list[WalletDTO] = await self._reader.read_by_user_id(
            user_id=target_user_id, sorting=query.sorting
        )
        if not wallets:
            raise UserNotFound

        return wallets
