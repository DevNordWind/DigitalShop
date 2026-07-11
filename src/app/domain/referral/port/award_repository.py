from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.referral.entity import ReferralAward
from app.domain.referral.value_object import ReferralAwardId


class ReferralAwardRepository(ABC):
    @abstractmethod
    async def add(self, award: ReferralAward) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, award_id: ReferralAwardId) -> ReferralAward | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_reference_id(self, reference_id: UUID) -> ReferralAward | None:
        raise NotImplementedError
