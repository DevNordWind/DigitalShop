from typing import Never

from app.common.port.file_storage import (
    FileIOError,
    FileNotFound,
    FilePermissionDenied,
    FileStorageError,
)
from frozendict import frozendict


class LocalFileStorageErrorMapper:
    MAPPING: frozendict[type[Exception], type[FileStorageError]] = frozendict(
        {
            FileNotFoundError: FileNotFound,
            PermissionError: FilePermissionDenied,
            IsADirectoryError: FileIOError,
            NotADirectoryError: FileIOError,
            FileExistsError: FileIOError,
            OSError: FileIOError,
        },
    )

    @classmethod
    def map(cls, orig_exc: Exception) -> type[FileStorageError] | None:
        for exc_type in type(orig_exc).__mro__:
            mapped = cls.MAPPING.get(exc_type)
            if mapped is not None:
                return mapped
        return None

    @classmethod
    def map_and_raise(cls, orig_exc: Exception) -> Never:
        mapped = cls.map(orig_exc)
        raise (
            mapped() if mapped is not None else FileStorageError()
        ) from orig_exc
