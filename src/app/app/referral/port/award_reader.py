from abc import ABC, abstractmethod

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.referral.dto.award import ReferralAwardDTO
from app.app.referral.dto.paginated import ReferralAwardsPaginated
from app.app.referral.dto.sorting import ReferralAwardSortingParams
from app.domain.referral.value_object import ReferralAwardId
from app.domain.user.value_object import UserId


class ReferralAwardReader(ABC):
    @abstractmethod
    async def read_by_referrer_id(
        self,
        referrer_id: UserId,
        sorting: ReferralAwardSortingParams,
        pagination: OffsetPaginationParams,
    ) -> ReferralAwardsPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_by_id(
        self,
        award_id: ReferralAwardId,
    ) -> ReferralAwardDTO | None:
        raise NotImplementedError
