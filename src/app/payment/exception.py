from app.common.exception import ApplicationError


class PaymentApplicationError(ApplicationError): ...


class PaymentNotFound(PaymentApplicationError): ...
