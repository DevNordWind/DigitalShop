from collections.abc import AsyncIterator
from dataclasses import dataclass

from domain.common.file import FileType


@dataclass(slots=True, frozen=True)
class FileKeyRawDTO:
    type: FileType
    content: AsyncIterator[bytes]
    extension: str | None


@dataclass(slots=True, frozen=True)
class FileKeyDTO:
    value: str
    type: FileType
