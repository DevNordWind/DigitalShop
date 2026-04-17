from abc import ABC, abstractmethod

from domain.referral.entity import ReferralAward
from domain.referral.value_object import ReferralAwardId


class ReferralAwardRepository(ABC):
    @abstractmethod
    async def add(self, award: ReferralAward) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, award_id: ReferralAwardId) -> ReferralAward | None:
        raise NotImplementedError
