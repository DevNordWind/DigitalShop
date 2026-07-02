from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.app.common.port.file_storage.dto import ResolvedKey
from app.domain.common.file_key import FileKey


class FileStorageReader(ABC):
    @abstractmethod
    async def read(self, key: FileKey) -> AsyncIterator[bytes]:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: FileKey) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def resolve(self, key: FileKey) -> ResolvedKey:
        raise NotImplementedError
