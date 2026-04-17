from dataclasses import dataclass

from app.common.port import DatabaseSession
from app.user.port import UserIdentifyProvider
from domain.common.money import Currency
from domain.referral.entity import ReferrerProfile
from domain.referral.port.profile_repository import ReferrerProfileRepository
from domain.referral.service import ReferrerProfileService


@dataclass(slots=True, frozen=True)
class CreateReferrerProfileCmd:
    award_currency: Currency
    send_notifications: bool


class CreateReferrerProfile:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        service: ReferrerProfileService,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: ReferrerProfileRepository = repo
        self._service: ReferrerProfileService = service
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: CreateReferrerProfileCmd) -> None:
        profile: ReferrerProfile = self._service.create(
            user_id=await self._idp.get_user_id(),
            award_currency=cmd.award_currency,
            send_notifications=cmd.send_notifications,
        )
        await self._repo.add(profile)

        await self._session.commit()
