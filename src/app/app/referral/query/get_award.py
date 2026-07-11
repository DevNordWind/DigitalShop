from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.referral.dto.award import ReferralAwardDTO
from app.app.referral.port import ReferralAwardReader
from app.domain.referral.exception import ReferralAwardNotFoundError
from app.domain.referral.service import ReferralAwardAccessService
from app.domain.referral.value_object import ReferralAwardId
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetReferralAwardQuery:
    id: UUID


class GetReferralAward:
    def __init__(self, reader: ReferralAwardReader, actor_provider: ActorProvider):
        self._reader: ReferralAwardReader = reader
        self._actor_provider = actor_provider

    async def __call__(self, query: GetReferralAwardQuery) -> ReferralAwardDTO:
        award: ReferralAwardDTO | None = await self._reader.read_by_id(
            award_id=ReferralAwardId(query.id),
        )
        if not award:
            raise ReferralAwardNotFoundError

        ReferralAwardAccessService.ensure_can_view(
            actor=await self._actor_provider.get(),
            referrer_id=UserId(award.referrer_id),
        )

        return award
