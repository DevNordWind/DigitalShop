from dataclasses import dataclass
from datetime import datetime

from domain.common.money import Money
from domain.payment.enums import (
    PaymentMethod,
    PaymentStatus,
)
from domain.payment.exception import (
    PaymentCancellationForbidden,
    PaymentConfirmationForbidden,
    PaymentFailureForbidden,
    PaymentStartForbidden,
)
from domain.payment.value_object import (
    CommissionSnapshot,
    PaymentExternalId,
    PaymentId,
    PaymentPurpose,
)
from domain.user.value_object import UserId


@dataclass(kw_only=True)
class Payment:
    id: PaymentId
    creator_id: UserId

    purpose: PaymentPurpose

    original_amount: Money
    commission_snapshot: CommissionSnapshot

    status: PaymentStatus = PaymentStatus.NEW

    method: PaymentMethod
    external_id: PaymentExternalId | None = None

    created_at: datetime
    updated_at: datetime | None = None

    @property
    def to_pay(self) -> Money:
        return self.original_amount + self.commission_snapshot.amount

    def start(
        self,
        external_id: PaymentExternalId,
        now: datetime,
    ) -> None:
        if self.status != PaymentStatus.NEW:
            raise PaymentStartForbidden

        self.status = PaymentStatus.PENDING
        self.external_id = external_id
        self.updated_at = now

    def confirm(self, now: datetime) -> None:
        if self.status != PaymentStatus.PENDING:
            raise PaymentConfirmationForbidden

        self.status = PaymentStatus.CONFIRMED
        self.updated_at = now

    def fail(self, now: datetime) -> None:
        if self.status not in (PaymentStatus.NEW, PaymentStatus.PENDING):
            raise PaymentFailureForbidden

        self.status = PaymentStatus.FAILED
        self.updated_at = now

    def cancel(self, now: datetime) -> None:
        if self.status not in (PaymentStatus.PENDING, PaymentStatus.NEW):
            raise PaymentCancellationForbidden

        self.status = PaymentStatus.CANCELLED
        self.updated_at = now
