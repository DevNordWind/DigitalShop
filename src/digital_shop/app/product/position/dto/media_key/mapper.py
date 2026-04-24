from app.common.dto.file_key import FileKeyDTO
from domain.product.position.value_object import PositionMediaKey


class PositionMediaKeyMapper:
    @classmethod
    def to_value_object(cls, src: FileKeyDTO) -> PositionMediaKey:
        return PositionMediaKey(value=src.value, type=src.type)
