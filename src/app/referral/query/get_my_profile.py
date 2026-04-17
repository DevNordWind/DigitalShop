from app.referral.dto.profile import ReferrerProfileDTO, ReferrerProfileMapper
from app.user.port import UserIdentifyProvider
from domain.referral.entity import ReferrerProfile
from domain.referral.port.profile_repository import ReferrerProfileRepository


class GetMyReferrerProfile:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        idp: UserIdentifyProvider,
    ):
        self._repo: ReferrerProfileRepository = repo
        self._idp: UserIdentifyProvider = idp

    async def __call__(self) -> ReferrerProfileDTO | None:
        profile: ReferrerProfile | None = await self._repo.get(
            user_id=await self._idp.get_user_id(),
        )
        if not profile:
            return None
        return ReferrerProfileMapper.to_dto(src=profile)
