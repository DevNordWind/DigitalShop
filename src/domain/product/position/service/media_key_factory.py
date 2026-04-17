from domain.common.file import FileKeyRaw
from domain.common.port import UUIDProvider
from domain.product.category.value_object import CategoryId
from domain.product.position.value_object import (
    PositionId,
    PositionMediaKey,
)


class PositionMediaKeyFactory:
    def __init__(self, uuid_provider: UUIDProvider):
        self._uuid: UUIDProvider = uuid_provider

    def generate(
        self,
        category_id: CategoryId,
        position_id: PositionId,
        raw: FileKeyRaw,
    ) -> PositionMediaKey:
        value = f"category/{category_id.value}/position/"
        value += f"{position_id.value}/{self._uuid()}"

        if raw.extension:
            value += f".{raw.extension.lower().removeprefix('.')}"

        return PositionMediaKey(value=value, type=raw.type)
