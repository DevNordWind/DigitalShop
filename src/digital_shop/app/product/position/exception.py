from app.common.exception import ApplicationError


class PositionApplicationError(ApplicationError): ...


class PositionNotFound(PositionApplicationError): ...


class PositionItemNotFound(PositionApplicationError): ...
