from dataclasses import dataclass

from app.common.dto.query_params import OffsetPaginationParams
from app.referral.dto.paginated import ReferralAwardsPaginated
from app.referral.dto.sorting import ReferralAwardSortingParams
from app.referral.port import ReferralAwardReader
from app.user.port import UserIdentifyProvider


@dataclass(slots=True, frozen=True)
class GetMyReferralAwardsQuery:
    sorting: ReferralAwardSortingParams
    pagination: OffsetPaginationParams


class GetMyReferralAwards:
    def __init__(self, reader: ReferralAwardReader, idp: UserIdentifyProvider):
        self._reader: ReferralAwardReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: GetMyReferralAwardsQuery,
    ) -> ReferralAwardsPaginated:
        return await self._reader.read_by_referrer_id(
            referrer_id=await self._idp.get_user_id(),
            sorting=query.sorting,
            pagination=query.pagination,
        )
