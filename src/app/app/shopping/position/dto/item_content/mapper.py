from app.app.shopping.position.dto.item_content import ItemContentDTO
from app.domain.shopping.position.item.value_object import ItemContent


class ItemContentMapper:
    @classmethod
    def to_dto(cls, src: ItemContent) -> ItemContentDTO:
        return ItemContentDTO(src.value)

    @classmethod
    def to_value_object(cls, src: ItemContentDTO) -> ItemContent:
        return ItemContent(src.value)
