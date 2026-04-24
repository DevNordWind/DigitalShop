from app.common.dto.file_key.dto import FileKeyDTO, FileKeyRawDTO
from domain.common.file import FileKey, FileKeyRaw


class FileKeyMapper:
    @classmethod
    def to_value_object(cls, src: FileKeyDTO) -> FileKey:
        return FileKey(value=src.value, type=src.type)

    @classmethod
    def to_dto(cls, src: FileKey) -> FileKeyDTO:
        return FileKeyDTO(value=src.value, type=src.type)


class FileKeyRawMapper:
    @classmethod
    def to_value_object(cls, src: FileKeyRawDTO) -> FileKeyRaw:
        return FileKeyRaw(type=src.type, extension=src.extension)
