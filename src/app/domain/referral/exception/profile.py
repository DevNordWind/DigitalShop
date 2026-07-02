from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDeniedError,
    EntityNotFoundError,
)


class ReferrerProfileError(DomainError): ...


class ReferrerProfilePermissionDeniedError(
    ReferrerProfileError, DomainPermissionDeniedError
): ...


class ReferrerProfileAlreadyExistsError(ReferrerProfileError, DomainConflictError): ...


class ReferrerProfileNotFoundError(ReferrerProfileError, EntityNotFoundError): ...
