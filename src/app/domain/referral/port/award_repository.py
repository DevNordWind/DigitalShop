from abc import ABC, abstractmethod

from app.domain.referral.entity import ReferralAward
from app.domain.referral.value_object import ReferralAwardId


class ReferralAwardRepository(ABC):
    @abstractmethod
    async def add(self, award: ReferralAward) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, award_id: ReferralAwardId) -> ReferralAward | None:
        raise NotImplementedError
