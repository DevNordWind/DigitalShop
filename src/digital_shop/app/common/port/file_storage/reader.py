from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.common.port.file_storage.dto import ResolvedKey
from domain.common.file import FileKey


class FileStorageReader(ABC):
    @abstractmethod
    async def get(self, key: FileKey) -> AsyncIterator[bytes]:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: FileKey) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def resolve(self, key: FileKey) -> ResolvedKey:
        raise NotImplementedError
