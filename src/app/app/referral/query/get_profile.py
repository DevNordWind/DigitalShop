from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.referral.dto.profile import ReferrerProfileDTO, ReferrerProfileMapper
from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.exception import ReferrerProfileNotFoundError
from app.domain.referral.port import ReferrerProfileRepository
from app.domain.referral.service.profile_access import ReferrerProfileAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetReferrerProfileQuery:
    target_user_id: UUID


class GetReferrerProfile:
    def __init__(self, repo: ReferrerProfileRepository, actor_provider: ActorProvider):
        self._repo = repo
        self._actor_provider = actor_provider

    async def __call__(self, query: GetReferrerProfileQuery) -> ReferrerProfileDTO:
        profile_user_id: UserId = UserId(query.target_user_id)

        ReferrerProfileAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), profile_user_id=profile_user_id
        )

        profile: ReferrerProfile | None = await self._repo.get(user_id=profile_user_id)
        if not profile:
            raise ReferrerProfileNotFoundError

        return ReferrerProfileMapper.to_dto(src=profile)
