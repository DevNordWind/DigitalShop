from app.domain.common.exception import DomainError, DomainPermissionDeniedError


class ReportError(DomainError): ...


class ReportPermissionDeniedError(ReportError, DomainPermissionDeniedError): ...
