from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence
from types import TracebackType
from typing import Self

from domain.common.file import FileKey


class FileStorageSession(ABC):
    @abstractmethod
    async def put(self, key: FileKey, content: AsyncIterator[bytes]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def put_many(
        self,
        keys: Sequence[tuple[FileKey, AsyncIterator[bytes]]],
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
