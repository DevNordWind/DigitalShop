from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path

from app.domain.common.file_key import FileKey


@dataclass(slots=True, frozen=True)
class File:
    key: FileKey
    content: AsyncIterator[bytes]


@dataclass(slots=True, frozen=True)
class ResolvedByPath:
    value: Path


@dataclass(slots=True, frozen=True)
class ResolvedByUrl:
    value: str


ResolvedKey = ResolvedByUrl | ResolvedByPath
