from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import FSInputFile, InputFile, URLInputFile
from aiogram_dialog.api.entities import MediaAttachment
from frozendict import frozendict

from app.common.port import FileStorageReader
from app.common.port.file_storage import (
    ResolvedByPath,
    ResolvedByUrl,
    ResolvedKey,
)
from domain.common.file import FileKey, FileType
from presentation.aiogram.mapper.file.exception import (
    UnsupportedContentType,
    UnsupportedFileType,
)


class FileTypeMapper:
    MAPPING: frozendict[ContentType, FileType] = frozendict(
        {
            ContentType.DOCUMENT: FileType.DOCUMENT,
            ContentType.ANIMATION: FileType.GIF,
            ContentType.PHOTO: FileType.PHOTO,
            ContentType.VIDEO: FileType.VIDEO,
        },
    )

    @classmethod
    def to_domain(cls, src: ContentType) -> FileType:
        tp = cls.MAPPING.get(src)
        if not tp:
            raise UnsupportedContentType(type=src)

        return tp

    @classmethod
    def to_aiogram(cls, src: FileType) -> ContentType:
        for k, v in cls.MAPPING.items():
            if v == src:
                return k
        raise UnsupportedFileType(type=src)


class FileKeyMapper:
    def __init__(self, reader: FileStorageReader):
        self._reader: FileStorageReader = reader

    async def to_media_attachment(self, key: FileKey) -> MediaAttachment:
        content_type: ContentType = FileTypeMapper.to_aiogram(src=key.type)
        resolved: ResolvedKey = await self._reader.resolve(key=key)

        match resolved:
            case ResolvedByPath(value=path):
                return MediaAttachment(type=content_type, path=path)
            case ResolvedByUrl(value=url):
                return MediaAttachment(type=content_type, url=url)

    async def to_input_file(self, key: FileKey, bot: Bot) -> InputFile:
        resolved: ResolvedKey = await self._reader.resolve(key=key)

        match resolved:
            case ResolvedByPath(value=path):
                return FSInputFile(path=path)
            case ResolvedByUrl(value=url):
                return URLInputFile(url=url, bot=bot)
