from abc import ABC, abstractmethod

from app.domain.referral.entity import ReferrerProfile
from app.domain.user.value_object import UserId


class ReferrerProfileRepository(ABC):
    @abstractmethod
    async def add(self, profile: ReferrerProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UserId) -> ReferrerProfile | None:
        raise NotImplementedError
