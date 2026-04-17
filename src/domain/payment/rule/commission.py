from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.common.coefficient import Coefficient
from domain.common.money import Money
from domain.payment.enums import CommissionType, PaymentMethod
from domain.payment.value_object import (
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
    def type(self) -> CommissionType:
        return CommissionType.CUSTOMER

    def calculate(self, amount: Money) -> Money:
        return Money(
            amount=amount.amount * self.coefficient.value,
            currency=amount.currency,
        )

    def take_snapshot(self, amount: Money) -> CommissionSnapshot:
        return CommissionSnapshot(
            type=self.type,
            amount=self.calculate(amount),
            coefficient=self.coefficient,
        )

    def change_coefficient(self, new_coefficient: Coefficient) -> None:
        self.coefficient = new_coefficient


@dataclass
class ShopCommissionRule(PaymentCommissionRule):
    @property
    def type(self) -> CommissionType:
        return CommissionType.SHOP

    def take_snapshot(self, amount: Money) -> CommissionSnapshot:
        return CommissionSnapshot(
            type=self.type,
            amount=self.calculate(amount),
            coefficient=None,
        )

    def calculate(self, amount: Money) -> Money:
        return Money.zero(
            currency=amount.currency,
        )
