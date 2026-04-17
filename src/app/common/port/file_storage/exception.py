from dataclasses import dataclass

from app.common.exception import ApplicationError


class FileStorageError(ApplicationError): ...


class FileNotFound(FileStorageError): ...


class FilePermissionDenied(FileStorageError): ...


class FileIOError(FileStorageError): ...


@dataclass
class FileTooLarge(FileStorageError):
    max_allowed_size: int


@dataclass
class FileKeyInvalid(FileStorageError):
    invalid_key: str


class FileStorageSessionError(FileStorageError): ...


class FileStorageSessionClosed(FileStorageSessionError): ...


class FileStorageSessionCommitError(FileStorageSessionError): ...
