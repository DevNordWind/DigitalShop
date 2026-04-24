from abc import ABC, abstractmethod

from domain.payment.enums import PaymentMethod
from domain.payment.rule import PaymentCommissionRule


class PaymentCommissionRuleRepository(ABC):
    @abstractmethod
    async def add(self, rule: PaymentCommissionRule) -> None:
        raise NotImplementedError

    @abstractmethod
    async def merge(
        self,
        old_rule: PaymentCommissionRule,
        new_rule: PaymentCommissionRule,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, method: PaymentMethod) -> PaymentCommissionRule:
        raise NotImplementedError
