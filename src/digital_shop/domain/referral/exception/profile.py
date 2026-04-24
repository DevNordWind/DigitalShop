from domain.common.exception import DomainError


class ReferrerProfileError(DomainError): ...


class ReferrerProfileAlreadyExists(ReferrerProfileError): ...
