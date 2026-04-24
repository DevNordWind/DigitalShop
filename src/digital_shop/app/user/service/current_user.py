from app.user.exception import UserAuthenticationError
from app.user.port import UserIdentifyProvider
from domain.user.entity import User
from domain.user.port import UserRepository


class GetCurrentUser:
    def __init__(self, idp: UserIdentifyProvider, repo: UserRepository):
        self._idp: UserIdentifyProvider = idp
        self._repo: UserRepository = repo

    async def __call__(self) -> User:
        user: User | None = await self._repo.get(
            user_id=await self._idp.get_user_id(),
        )
        if not user:
            raise UserAuthenticationError

        return user
