import asyncio
import logging
from collections.abc import AsyncIterator
from pathlib import Path
from typing import cast

from aiofile import AIOFile

from app.common.port.file_storage import (
    FileKeyInvalid,
    FileNotFound,
    FileStorageReader,
)
from app.common.port.file_storage.dto import ResolvedByPath, ResolvedKey
from domain.common.file import FileKey
from infra.common.file_storage.mapper import LocalFileStorageErrorMapper

logger = logging.getLogger(__name__)


class FileSystemReader(FileStorageReader):
    def __init__(
        self,
        base_path: Path,
        *,
        chunk_size: int = 1024 * 1024,
    ) -> None:
        self._base_path = Path(base_path).resolve()
        self._chunk_size = chunk_size

    async def get(self, key: FileKey) -> AsyncIterator[bytes]:
        path: Path = self._resolve(key)
        logger.debug("GET start", extra={"key": key.value})

        async def _reader() -> AsyncIterator[bytes]:
            try:
                async with AIOFile(path, "rb") as afp:
                    while chunk := await afp.read(self._chunk_size):
                        yield cast("bytes", chunk)

                logger.info("GET success", extra={"key": key.value})
            except FileNotFoundError as e:
                logger.warning(
                    "GET failed: file not found",
                    extra={"key": key.value},
                )
                raise FileNotFound(key.value) from e
            except Exception as e:
                logger.exception("GET failed", extra={"key": key.value})
                LocalFileStorageErrorMapper.map_and_raise(e)

        return _reader()

    async def exists(self, key: FileKey) -> bool:
        path = self._resolve(key)

        return await asyncio.to_thread(path.exists)

    async def resolve(self, key: FileKey) -> ResolvedKey:
        path = self._resolve(key)
        if not await asyncio.to_thread(path.exists):
            raise FileNotFound(key.value)

        return ResolvedByPath(value=path)

    def _resolve(self, key: FileKey) -> Path:
        path = (self._base_path / key.value).resolve()
        if not path.is_relative_to(self._base_path):
            raise FileKeyInvalid(invalid_key=key.value)

        return path
