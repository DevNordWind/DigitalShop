from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from uuid import UUID

from app.common.dto.money import MoneyDTO
from domain.payment.enums import PaymentMethod


class InvoiceStatus(StrEnum):
    PENDING = "PENDING"
    PAID = "PAID"


@dataclass(slots=True, frozen=True)
class CreateInvoice:
    payment_id: UUID
    to_pay: MoneyDTO

    expires_in: timedelta = timedelta(hours=3)


@dataclass(slots=True, frozen=True)
class GetInvoice:
    invoice_id: str


@dataclass(slots=True, frozen=True)
class CancelInvoice:
    invoice_id: str


@dataclass(slots=True, frozen=True)
class Invoice:
    payment_id: UUID
    invoice_id: str

    payment_method: PaymentMethod
    status: InvoiceStatus | str
    pay_url: str

    to_pay: MoneyDTO
