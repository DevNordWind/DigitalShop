from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.user.dto import UserProfileDTO
from app.app.user.port import UserIdentifyResolver, UserReader
from app.domain.user.exception import UserNotFoundError
from app.domain.user.service import UserAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetUserProfileQuery:
    target_identifier: str | UUID


class GetUserProfile:
    def __init__(
        self,
        reader: UserReader,
        actor_provider: ActorProvider,
        idr: UserIdentifyResolver,
    ):
        self._reader = reader
        self._actor_provider = actor_provider
        self._idr: UserIdentifyResolver = idr

    async def __call__(self, query: GetUserProfileQuery) -> UserProfileDTO:
        target_user_id: UserId | None = await self._idr.resolve(
            identifier=query.target_identifier
        )
        if target_user_id is None:
            raise UserNotFoundError

        UserAccessService.ensure_can_view_profile(
            actor=await self._actor_provider.get(), target_user_id=target_user_id
        )

        user_profile: UserProfileDTO | None = await self._reader.read_profile(
            user_id=target_user_id
        )
        if not user_profile:
            raise UserNotFoundError

        return user_profile
