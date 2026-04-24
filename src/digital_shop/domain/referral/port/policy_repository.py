from abc import ABC, abstractmethod

from domain.referral.policy import ReferralPolicy


class ReferralPolicyRepository(ABC):
    @abstractmethod
    async def add(self, policy: ReferralPolicy) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> ReferralPolicy:
        raise NotImplementedError

    @abstractmethod
    async def get_for_update(self) -> ReferralPolicy:
        raise NotImplementedError
