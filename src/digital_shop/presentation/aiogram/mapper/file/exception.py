from dataclasses import dataclass

from aiogram.enums import ContentType
from domain.common.file import FileType
from presentation.aiogram.mapper.exception import AiogramMappingError


class FileMappingError(AiogramMappingError): ...


@dataclass(slots=True, frozen=True)
class UnsupportedContentType(FileMappingError):
    type: ContentType


class MessageNotContainFile(FileMappingError): ...


@dataclass(slots=True, frozen=True)
class UnsupportedFileType(FileMappingError):
    type: FileType


@dataclass(slots=True, frozen=True)
class TelegramFileDownloadError(FileMappingError):
    file_id: str


class InvalidMediaAttachment(FileMappingError): ...
