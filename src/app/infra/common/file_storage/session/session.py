import asyncio
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self, override
from uuid import uuid7

from app.app.common.port.file_storage import (
    File,
    FileStorageSession,
    FileStorageSessionClosedError,
    FileStorageSessionCommitError,
)
from app.domain.common.file_key import FileKey
from app.infra.common.file_storage.session.writer import FileSystemWriter

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PendingPut:
    temp_key: FileKey
    final_key: FileKey


@dataclass(frozen=True, slots=True)
class PendingDelete:
    key: FileKey


class FileSystemStorageSession(FileStorageSession):
    def __init__(
        self,
        writer: FileSystemWriter,
        temp_prefix: Path = Path("tmp/sessions"),
    ) -> None:
        self._writer = writer
        self._temp_path: Path = writer.base_path / temp_prefix

        self._puts: list[PendingPut] = []
        self._deletes: list[PendingDelete] = []
        self._done = False

    @override
    async def put(self, file: File) -> None:
        self._guard()
        temp_key = self._make_temp_key(file.key)

        await self._writer.put(file)

        self._puts.append(PendingPut(temp_key=temp_key, final_key=file.key))
        logger.debug(
            "SESSION put staged",
            extra={"key": file.key.value, "temp": temp_key.value},
        )

    @override
    async def put_many(
        self,
        files: Sequence[File],
    ) -> None:
        self._guard()
        await asyncio.gather(
            *[self.put(file=file) for file in files],
        )

    @override
    async def delete(self, key: FileKey) -> None:
        self._guard()
        self._deletes.append(PendingDelete(key=key))
        logger.debug("SESSION delete staged", extra={"key": key.value})

    @override
    async def commit(self) -> None:
        self._guard()
        self._done = True

        try:
            await asyncio.gather(
                *[self._writer.move(op.temp_key, op.final_key) for op in self._puts],
            )
        except Exception as e:
            await self._cleanup_puts()
            logger.exception("SESSION commit failed during puts")
            raise FileStorageSessionCommitError from e

        try:
            await asyncio.gather(
                *[self._writer.delete(op.key) for op in self._deletes],
            )
        except Exception as e:
            logger.exception("SESSION commit failed during deletes")
            raise FileStorageSessionCommitError from e

        logger.info(
            "SESSION committed",
            extra={"puts": len(self._puts), "deletes": len(self._deletes)},
        )

    @override
    async def rollback(self) -> None:
        if self._done:
            return

        self._done = True
        await self._cleanup_puts()
        logger.info("SESSION rolled back", extra={"puts": len(self._puts)})

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    def _make_temp_key(self, key: FileKey) -> FileKey:
        temp_path = self._temp_path / uuid7().hex / key.value
        relative = temp_path.relative_to(self._writer.base_path)

        return FileKey(
            value=str(relative),
            type=key.type,
        )

    def _guard(self) -> None:
        if self._done:
            raise FileStorageSessionClosedError

    async def _cleanup_puts(self) -> None:
        await asyncio.gather(
            *[self._writer.delete(op.temp_key) for op in self._puts],
            return_exceptions=True,
        )
