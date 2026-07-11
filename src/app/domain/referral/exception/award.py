from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
    EntityNotFoundError,
)


class ReferralAwardError(DomainError): ...


class ReferralAwardNotFoundError(ReferralAwardError, EntityNotFoundError): ...


class ReferralAwardPermissionDeniedError(
    ReferralAwardError, DomainPermissionDeniedError
): ...
