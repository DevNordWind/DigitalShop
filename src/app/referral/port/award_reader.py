from abc import ABC, abstractmethod

from app.common.dto.query_params import OffsetPaginationParams
from app.referral.dto.award import ReferralAwardDTO
from app.referral.dto.paginated import ReferralAwardsPaginated
from app.referral.dto.sorting import ReferralAwardSortingParams
from domain.referral.value_object import ReferralAwardId
from domain.user.value_object import UserId


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
