from dataclasses import dataclass
from uuid import UUID

from app.referral.dto.award import ReferralAwardDTO
from app.referral.exception import ReferralAwardNotFound
from app.referral.port import ReferralAwardReader
from app.user.port import UserIdentifyProvider
from domain.referral.exception import ReferralAwardPermissionDenied
from domain.referral.service import ReferralAwardAccessService
from domain.referral.value_object import ReferralAwardId
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetReferralAwardQuery:
    id: UUID


class GetReferralAward:
    def __init__(self, reader: ReferralAwardReader, idp: UserIdentifyProvider):
        self._reader: ReferralAwardReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: GetReferralAwardQuery) -> ReferralAwardDTO:
        award: ReferralAwardDTO | None = await self._reader.read_by_id(
            award_id=ReferralAwardId(query.id),
        )
        if not award:
            raise ReferralAwardNotFound

        if not ReferralAwardAccessService.can_view(
            referrer_id=UserId(award.referrer_id),
            viewer_role=await self._idp.get_role(),
            viewer_id=await self._idp.get_user_id(),
        ):
            raise ReferralAwardPermissionDenied

        return award
