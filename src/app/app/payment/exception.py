from app.app.common.exception import AppError, BootstrapError


class PaymentAppError(AppError): ...


class PaymentCommissionRuleNotCreatedError(PaymentAppError, BootstrapError): ...
