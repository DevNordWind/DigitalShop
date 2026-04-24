from app.common.port import DatabaseSession
from app.referral.exception import ReferrerProfileNotFound
from app.user.port import UserIdentifyProvider
from domain.referral.entity import ReferrerProfile
from domain.referral.port.profile_repository import ReferrerProfileRepository


class SwitchReferrerProfileNotifications:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: ReferrerProfileRepository = repo
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
    ) -> None:
        profile: ReferrerProfile | None = await self._repo.get(
            user_id=await self._idp.get_user_id(),
        )
        if not profile:
            raise ReferrerProfileNotFound

        profile.switch_send_notifications()
        await self._session.commit()
