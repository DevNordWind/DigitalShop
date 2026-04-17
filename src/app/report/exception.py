from app.common.exception import ApplicationError


class ReporterApplicationError(ApplicationError): ...


class ReporterPermissionDenied(ReporterApplicationError): ...
