import asyncio
import logging
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import uuid7

from aiofile import AIOFile

from app.common.port.file_storage import (
    FileKeyInvalid,
    FileStorageError,
    FileTooLarge,
)
from domain.common.file import FileKey
from infra.common.file_storage.mapper import LocalFileStorageErrorMapper

logger = logging.getLogger(__name__)


class FileSystemWriter:
    def __init__(
        self,
        base_path: Path,
        *,
        max_concurrency: int = 5,
        chunk_size: int = 1024 * 1024,
        max_file_size: int | None = None,
    ) -> None:
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

        self._chunk_size = chunk_size
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._max_file_size = max_file_size

    async def put(self, key: FileKey, content: AsyncIterator[bytes]) -> None:
        async with self._semaphore:
            path = self._resolve(key)
            try:
                await self._write_atomic(path, content)
            except FileStorageError:
                raise
            except Exception as e:
                LocalFileStorageErrorMapper.map_and_raise(orig_exc=e)

    async def move(self, source: FileKey, destination: FileKey) -> None:
        src: Path = self._resolve(source)
        dst: Path = self._resolve(destination)

        try:
            await self._mkdir(dst.parent)
            await self._replace(src, dst)
        except FileStorageError:
            raise
        except Exception as e:
            LocalFileStorageErrorMapper.map_and_raise(e)

    async def delete(self, key: FileKey) -> None:
        path = self._resolve(key)
        try:
            await asyncio.to_thread(path.unlink, missing_ok=True)
        except Exception as e:
            LocalFileStorageErrorMapper.map_and_raise(e)

    def _resolve(self, key: FileKey) -> Path:
        path = (self.base_path / key.value).resolve()
        if not path.is_relative_to(self.base_path):
            raise FileKeyInvalid(key.value)

        return path

    async def _write_atomic(
        self,
        path: Path,
        content: AsyncIterator[bytes],
    ) -> None:
        await self._mkdir(path.parent)
        temp_path = path.with_name(f"{path.name}.{uuid7().hex}.tmp")
        size: int = 0

        try:
            async with AIOFile(temp_path, "wb") as afp:
                async for chunk in content:
                    if not chunk:
                        continue
                    size += len(chunk)
                    if (
                        self._max_file_size is not None
                        and size > self._max_file_size
                    ):
                        raise FileTooLarge(
                            max_allowed_size=self._max_file_size,
                        )
                    await afp.write(chunk)
                await afp.fsync()

            await self._replace(temp_path, path)

        except Exception:
            await self._unlink(temp_path)
            raise

    async def _mkdir(self, path: Path) -> None:
        await asyncio.to_thread(path.mkdir, parents=True, exist_ok=True)

    async def _replace(self, src: Path, dst: Path) -> None:
        await asyncio.to_thread(src.replace, dst)

    async def _unlink(self, path: Path) -> None:
        await asyncio.to_thread(path.unlink, missing_ok=True)
