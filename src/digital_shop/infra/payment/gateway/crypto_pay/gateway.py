import logging

from aiocryptopay import AioCryptoPay  # type: ignore[import-untyped]
from aiocryptopay.const import CurrencyType  # type: ignore[import-untyped]
from aiocryptopay.exceptions import (  # type: ignore[import-untyped]
    CodeErrorFactory,
)
from aiocryptopay.models.invoice import (  # type: ignore[import-untyped]
    Invoice as CryptoBotInvoice,
)
from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
)
from app.payment.port.payment import (
    CancelInvoice,
    CreateInvoice,
    GetInvoice,
    InvalidInvoiceId,
    Invoice,
    InvoiceNotFound,
)
from infra.payment.gateway.crypto_pay.mapper import CryptoPayInvoiceMapper

logger = logging.getLogger(__name__)


class CryptoPayPaymentGateway(PaymentMethodGateway):
    def __init__(self, aio_cryptopay: AioCryptoPay):
        self._aio_cryptopay: AioCryptoPay = aio_cryptopay

    async def create(self, data: CreateInvoice) -> Invoice:
        try:
            crypto_pay_invoice: CryptoBotInvoice = (
                await self._aio_cryptopay.create_invoice(
                    amount=float(str(data.to_pay.amount)),
                    payload=str(data.payment_id),
                    fiat=data.to_pay.currency,
                    currency_type=CurrencyType.FIAT,
                    expires_in=data.expires_in.seconds,
                )
            )
        except CodeErrorFactory as e:
            logger.error(e)
            raise PaymentMethodGatewayError from e

        return CryptoPayInvoiceMapper.to_invoice(src=crypto_pay_invoice)

    async def get(self, data: GetInvoice) -> Invoice:
        try:
            invoice_id = int(data.invoice_id)
        except ValueError as e:
            raise InvalidInvoiceId from e

        try:
            crypto_pay_invoice: (
                CryptoBotInvoice | list[CryptoBotInvoice] | None
            ) = await self._aio_cryptopay.get_invoices(invoice_ids=invoice_id)
            if crypto_pay_invoice is None:
                raise InvoiceNotFound

            if isinstance(crypto_pay_invoice, list):
                try:
                    crypto_pay_invoice = crypto_pay_invoice[0]
                except IndexError as e:
                    raise InvoiceNotFound from e

        except CodeErrorFactory as e:
            raise PaymentMethodGatewayError from e

        return CryptoPayInvoiceMapper.to_invoice(src=crypto_pay_invoice)

    async def cancel(self, data: CancelInvoice) -> bool:
        try:
            invoice_id = int(data.invoice_id)
        except ValueError as e:
            raise InvalidInvoiceId from e

        try:
            return await self._aio_cryptopay.delete_invoice(  # type: ignore[no-any-return]
                invoice_id=invoice_id,
            )
        except CodeErrorFactory as e:
            raise PaymentMethodGatewayError from e
