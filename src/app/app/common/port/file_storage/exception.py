from dataclasses import dataclass

from app.app.common.exception import AppInfrastructureError


class FileStorageError(AppInfrastructureError): ...


class FileStorageFileNotFoundError(FileStorageError): ...


class FilePermissionDeniedError(FileStorageError): ...


class FileIOError(FileStorageError): ...


@dataclass
class FileTooLargeError(FileStorageError):
    max_allowed_size: int


@dataclass
class FileKeyInvalidError(FileStorageError):
    invalid_key: str


class FileStorageSessionError(FileStorageError): ...


class FileStorageSessionClosedError(FileStorageSessionError): ...


class FileStorageSessionCommitError(FileStorageSessionError): ...
