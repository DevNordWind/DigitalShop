from domain.common.file import FileKeyRaw
from domain.common.port import UUIDProvider
from domain.product.category.value_object import (
    CategoryId,
    CategoryMediaKey,
)


class CategoryMediaKeyFactory:
    def __init__(self, uuid_provider: UUIDProvider):
        self._uuid: UUIDProvider = uuid_provider

    def generate(
        self,
        raw: FileKeyRaw,
        category_id: CategoryId,
    ) -> CategoryMediaKey:
        value = f"category/{category_id.value}/{self._uuid()}"

        if raw.extension:
            value += f".{raw.extension.lower().removeprefix('.')}"

        return CategoryMediaKey(type=raw.type, value=value)
