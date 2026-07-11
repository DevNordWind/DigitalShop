from abc import ABC, abstractmethod

from app.domain.payment.enums import PaymentMethod
from app.domain.payment.rule import PaymentCommissionRule


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
