from decimal import Decimal
from uuid import UUID

from aiocryptopay.models.invoice import (  # type: ignore[import-untyped]
    Invoice as CryptoBotInvoice,
)
from frozendict import frozendict

from app.common.dto.money import MoneyDTO
from app.payment.port.payment import Invoice
from app.payment.port.payment.dto import InvoiceStatus
from domain.common.money import Currency
from domain.payment.enums import PaymentMethod


class CryptoPayInvoiceMapper:
    STATUS_MAPPING: frozendict[str, InvoiceStatus] = frozendict(
        {
            "active": InvoiceStatus.PENDING,
            "paid": InvoiceStatus.PAID,
        },
    )

    @classmethod
    def to_invoice(cls, src: CryptoBotInvoice) -> Invoice:
        return Invoice(
            invoice_id=str(src.invoice_id),
            status=cls.STATUS_MAPPING.get(src.status, src.status),
            payment_id=UUID(src.payload),
            pay_url=src.bot_invoice_url,
            to_pay=MoneyDTO(
                amount=Decimal(str(src.amount)),
                currency=Currency(src.fiat),
            ),
            payment_method=PaymentMethod.CRYPTO_PAY,
        )
