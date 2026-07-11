from app.domain.common.money import Money
from app.domain.common.port import Clock, UUIDProvider
from app.domain.payment.entity import Payment
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.rule import PaymentCommissionRule
from app.domain.payment.value_object import (
    PaymentId,
    PaymentPurpose,
)
from app.domain.user.value_object import UserId


class PaymentDomainService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        creator_id: UserId,
        purpose: PaymentPurpose,
        method: PaymentMethod,
        amount: Money,
        commission_rule: PaymentCommissionRule,
    ) -> Payment:
        return Payment(
            id=PaymentId(self._uuid()),
            creator_id=creator_id,
            purpose=purpose,
            original_amount=amount,
            commission_snapshot=commission_rule.take_snapshot(amount=amount),
            method=method,
            created_at=self._clock.now(),
        )
