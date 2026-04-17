from domain.common.exception import DomainError


class UserError(DomainError): ...


class UserPermissionDenied(UserError): ...
