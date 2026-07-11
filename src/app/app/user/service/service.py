from app.app.common.port.session import DatabaseSession
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.port import UserRepository
from app.domain.user.service import UserDomainService
from app.domain.user.service.service import RegisteredUser
from app.domain.user.value_object import UserId
from app.domain.wallet.port import WalletRepository


class UserApplicationService:
    def __init__(
        self,
        service: UserDomainService,
        session: DatabaseSession,
        user_repo: UserRepository,
        wallet_repo: WalletRepository,
    ):
        self._service = service
        self._session = session
        self._user_repo = user_repo
        self._wallet_repo = wallet_repo

    async def register(self, role: UserRole, referrer_id: UserId | None) -> User:
        registered_user: RegisteredUser = self._service.register(
            role=role, referrer_id=referrer_id
        )
        await self._user_repo.add(user=registered_user.user)
        await self._session.flush()
        await self._wallet_repo.add_many(wallets=registered_user.wallets)

        return registered_user.user
