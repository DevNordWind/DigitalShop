from app.app.common.exception import AppError, BootstrapError


class ReferralAppError(AppError): ...


class ReferralPolicyNotCreatedError(ReferralAppError, BootstrapError): ...
