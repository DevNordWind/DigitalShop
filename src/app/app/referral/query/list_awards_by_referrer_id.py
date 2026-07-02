from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.referral.dto.paginated import ReferralAwardsPaginated
from app.app.referral.dto.sorting import ReferralAwardSortingParams
from app.app.referral.port import ReferralAwardReader
from app.domain.referral.service import ReferralAwardAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class ListReferralAwardsQuery:
    referrer_id: UUID

    sorting: ReferralAwardSortingParams
    pagination: OffsetPaginationParams


class ListReferralAwards:
    def __init__(self, reader: ReferralAwardReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: ListReferralAwardsQuery,
    ) -> ReferralAwardsPaginated:
        referrer_id: UserId = UserId(query.referrer_id)

        ReferralAwardAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), referrer_id=referrer_id
        )

        return await self._reader.read_by_referrer_id(
            referrer_id=referrer_id,
            sorting=query.sorting,
            pagination=query.pagination,
        )
