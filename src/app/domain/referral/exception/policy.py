from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
)


class ReferralPolicyError(DomainError): ...


class ReferralPolicyPermissionDeniedError(
    ReferralPolicyError, DomainPermissionDeniedError
): ...
