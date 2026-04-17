from domain.common.exception import ValueObjectError


class PaymentSourceError(ValueObjectError): ...


class PaymentIdRequired(PaymentSourceError): ...
