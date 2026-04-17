from dataclasses import dataclass

from app.common.port import DatabaseSession
from app.referral.exception import ReferrerProfileNotFound
from app.user.port import UserIdentifyProvider
from domain.common.money import Currency
from domain.referral.entity import ReferrerProfile
from domain.referral.port.profile_repository import ReferrerProfileRepository


@dataclass(slots=True, frozen=True)
class ChangeReferrerProfileAwardCurrencyCmd:
    new_currency: Currency


class ChangeReferrerProfileAwardCurrency:
    def __init__(
        self,
        repo: ReferrerProfileRepository,
        sesssion: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: ReferrerProfileRepository = repo
        self._session: DatabaseSession = sesssion
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        cmd: ChangeReferrerProfileAwardCurrencyCmd,
    ) -> None:
        profile: ReferrerProfile | None = await self._repo.get(
            user_id=await self._idp.get_user_id(),
        )
        if not profile:
            raise ReferrerProfileNotFound

        profile.change_award_currency(new_currency=cmd.new_currency)
        await self._session.commit()
