from app.domain.common.file_key import FileKeyError


class PositionMediaKeyError(FileKeyError): ...


class PositionMediaKeyMustBeMediaError(PositionMediaKeyError): ...
