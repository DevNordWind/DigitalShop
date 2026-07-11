from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.exception import ReferrerProfileNotFoundError
from app.domain.referral.port import ReferrerProfileRepository
from app.domain.referral.service.profile_access import ReferrerProfileAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class SwitchReferrerProfileNotificationsCmd:
    target_user_id: UUID


class SwitchReferrerProfileNotifications:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repo = repo
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: SwitchReferrerProfileNotificationsCmd) -> None:
        target_user_id: UserId = UserId(cmd.target_user_id)
        ReferrerProfileAccessService.ensure_can_change(
            actor=await self._actor_provider.get(), profile_user_id=target_user_id
        )
        profile: ReferrerProfile | None = await self._repo.get(user_id=target_user_id)
        if not profile:
            raise ReferrerProfileNotFoundError

        profile.switch_send_notifications()
        await self._session.commit()
