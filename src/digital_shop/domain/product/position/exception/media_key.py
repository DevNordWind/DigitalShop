from domain.common.file import FileKeyError


class PositionMediaKeyError(FileKeyError): ...


class PositionMediaKeyMustBeMediaError(PositionMediaKeyError): ...


class PositionMediaNotFound(PositionMediaKeyError): ...
