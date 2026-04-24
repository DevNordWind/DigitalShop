from domain.common.money import Money
from domain.common.port import Clock, UUIDProvider
from domain.payment.entity import Payment
from domain.payment.enums import PaymentMethod
from domain.payment.rule import PaymentCommissionRule
from domain.payment.value_object import (
    CommissionSnapshot,
    PaymentId,
    PaymentPurpose,
)
from domain.user.entity import User


class PaymentService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        creator: User,
        purpose: PaymentPurpose,
        method: PaymentMethod,
        amount: Money,
        commission_rule: PaymentCommissionRule,
    ) -> Payment:
        commission_snapshot: CommissionSnapshot = (
            commission_rule.take_snapshot(
                amount=amount,
            )
        )

        return Payment(
            id=PaymentId(self._uuid()),
            creator_id=creator.id,
            purpose=purpose,
            original_amount=amount,
            commission_snapshot=commission_snapshot,
            method=method,
            created_at=self._clock.now(),
        )
