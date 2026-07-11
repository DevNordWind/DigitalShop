from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
    EntityNotFoundError,
)


class UserError(DomainError): ...


class UserNotFoundError(UserError, EntityNotFoundError): ...


class UserPermissionDeniedError(UserError, DomainPermissionDeniedError): ...
