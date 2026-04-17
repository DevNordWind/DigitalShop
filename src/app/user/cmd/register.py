from copy import copy
from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from domain.user.enums import UserRole
from domain.user.port import UserRepository
from domain.user.service import UserService
from domain.user.value_object import UserId
from domain.wallet.port import WalletRepository


@dataclass(slots=True, frozen=True)
class RegisterUserCmd:
    referrer_id: UUID | None
    role: UserRole


class RegisterUser:
    def __init__(
        self,
        user_repo: UserRepository,
        wallet_repo: WalletRepository,
        session: DatabaseSession,
        service: UserService,
    ):
        self._user_repo: UserRepository = user_repo
        self._wallet_repo: WalletRepository = wallet_repo
        self._session: DatabaseSession = session
        self._service: UserService = service

    async def __call__(self, cmd: RegisterUserCmd) -> UserId:
        user, wallets = self._service.register(
            role=cmd.role,
            referrer_id=UserId(cmd.referrer_id)
            if cmd.referrer_id is not None
            else None,
        )

        user_id: UserId = copy(user.id)
        await self._user_repo.add(user=user)
        await self._wallet_repo.add_many(wallets=wallets)
        await self._session.commit()

        return user_id
