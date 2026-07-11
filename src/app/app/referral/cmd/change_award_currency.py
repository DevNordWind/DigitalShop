from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.money import Currency
from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.exception import ReferrerProfileNotFoundError
from app.domain.referral.port import ReferrerProfileRepository
from app.domain.referral.service.profile_access import ReferrerProfileAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class ChangeReferrerProfileAwardCurrencyCmd:
    user_id: UUID
    new_currency: Currency


class ChangeReferrerProfileAwardCurrency:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repo = repo
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(
        self,
        cmd: ChangeReferrerProfileAwardCurrencyCmd,
    ) -> None:
        user_id = UserId(cmd.user_id)

        ReferrerProfileAccessService.ensure_can_change(
            actor=await self._actor_provider.get(), profile_user_id=user_id
        )
        profile: ReferrerProfile | None = await self._repo.get(user_id=user_id)
        if not profile:
            raise ReferrerProfileNotFoundError

        profile.change_award_currency(new_currency=cmd.new_currency)
        await self._session.commit()
