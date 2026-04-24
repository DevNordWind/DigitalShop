from dataclasses import dataclass

from domain.common.exception import ValueObjectError


class FileKeyError(ValueObjectError): ...


@dataclass(slots=True, frozen=True)
class FileKeyTooLongError(FileKeyError):
    max_length: int


class FileKeyAlreadyExists(FileKeyError): ...


class FileKeyInvalidFormatError(FileKeyError): ...
