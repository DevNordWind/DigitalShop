from dataclasses import dataclass

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.actor import UserActor
from app.domain.common.money import Currency
from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.port import ReferrerProfileRepository
from app.domain.referral.service import ReferrerProfileDomainService
from app.domain.referral.service.profile_access import ReferrerProfileAccessService


@dataclass(slots=True, frozen=True)
class CreateReferrerProfileCmd:
    award_currency: Currency
    send_notifications: bool


class CreateReferrerProfile:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        service: ReferrerProfileDomainService,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repo = repo
        self._service = service
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: CreateReferrerProfileCmd) -> None:
        actor: UserActor = ReferrerProfileAccessService.ensure_can_create(
            actor=await self._actor_provider.get(),
        )

        profile: ReferrerProfile = self._service.create(
            user_id=actor.id,
            award_currency=cmd.award_currency,
            send_notifications=cmd.send_notifications,
        )
        await self._repo.add(profile=profile)

        await self._session.commit()
