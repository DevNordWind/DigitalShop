from abc import ABC, abstractmethod
from collections.abc import Sequence
from types import TracebackType
from typing import Self

from app.app.common.port.file_storage.dto import File
from app.domain.common.file_key import FileKey


class FileStorageSession(ABC):
    @abstractmethod
    async def put(self, file: File) -> None:
        raise NotImplementedError

    @abstractmethod
    async def put_many(
        self,
        files: Sequence[File],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: FileKey) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError
