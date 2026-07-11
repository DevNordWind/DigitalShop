from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from app.domain.common.coefficient import Coefficient
from app.domain.common.money import Money
from app.domain.payment.enums import CommissionType, PaymentMethod
from app.domain.payment.value_object import (
    CommissionSnapshot,
)


@dataclass
class PaymentCommissionRule(ABC):
    payment_method: PaymentMethod

    @property
    @abstractmethod
    def type(self) -> CommissionType:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, amount: Money) -> Money:
        raise NotImplementedError

    @abstractmethod
    def take_snapshot(self, amount: Money) -> CommissionSnapshot:
        raise NotImplementedError


@dataclass
class CustomerCommissionRule(PaymentCommissionRule):
    coefficient: Coefficient

    @property
    @override
    def type(self) -> CommissionType:
        return CommissionType.CUSTOMER

    @override
    def calculate(self, amount: Money) -> Money:
        return Money(
            amount=amount.amount * self.coefficient.value,
            currency=amount.currency,
        )

    @override
    def take_snapshot(self, amount: Money) -> CommissionSnapshot:
        return CommissionSnapshot(
            type=self.type,
            amount=self.calculate(amount),
            coefficient=self.coefficient,
        )

    def create_with_new_coefficient(
        self, new_coefficient: Coefficient
    ) -> CustomerCommissionRule:
        return CustomerCommissionRule(
            payment_method=self.payment_method, coefficient=new_coefficient
        )


@dataclass
class ShopCommissionRule(PaymentCommissionRule):
    @property
    @override
    def type(self) -> CommissionType:
        return CommissionType.SHOP

    @override
    def take_snapshot(self, amount: Money) -> CommissionSnapshot:
        return CommissionSnapshot(
            type=self.type,
            amount=self.calculate(amount),
            coefficient=None,
        )

    @override
    def calculate(self, amount: Money) -> Money:
        return Money.zero(
            currency=amount.currency,
        )
