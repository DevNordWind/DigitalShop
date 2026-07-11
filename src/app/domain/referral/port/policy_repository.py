from abc import ABC, abstractmethod

from app.domain.referral.policy import ReferralPolicy


class ReferralPolicyRepository(ABC):
    @abstractmethod
    async def add(self, policy: ReferralPolicy) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> ReferralPolicy:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self) -> ReferralPolicy:
        raise NotImplementedError
