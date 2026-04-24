from domain.product.position.item.value_object import (
    ItemContent,
    ItemRaw,
    TextItem,
)


class ItemContentFactory:
    def create(
        self,
        raw: ItemRaw,
    ) -> ItemContent:
        if isinstance(raw.value, str):
            return TextItem(raw.value)

        raise ValueError("Unsupported ItemRaw value")
