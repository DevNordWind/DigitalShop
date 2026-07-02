from app.app.common.exception import AppExternalServiceError
from app.app.payment.exception import PaymentAppError


class PaymentMethodGatewayError(PaymentAppError, AppExternalServiceError): ...


class UnsupportedPaymentMethodError(PaymentMethodGatewayError): ...


class InvalidInvoiceIdError(PaymentMethodGatewayError): ...


class InvoiceNotFoundError(PaymentMethodGatewayError): ...
