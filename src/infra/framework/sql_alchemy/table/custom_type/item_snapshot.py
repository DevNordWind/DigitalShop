from uuid import UUID

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from domain.order.value_object import ItemSnapshot
from domain.product.position.item.value_object import TextItem


class ItemSnapshotType(TypeDecorator[ItemSnapshot]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: ItemSnapshot | None,
        dialect: Dialect,
    ) -> dict[str, str] | None:
        if value is None:
            return None

        if not isinstance(value.item_content, TextItem):
            raise ValueError(f"Unsupported ItemContent: {value.item_content}")

        return {
            "item_id": str(value.item_id),
            "item_content": value.item_content.value,
        }

    def process_result_value(
        self,
        value: dict[str, str] | None,
        dialect: Dialect,
    ) -> ItemSnapshot | None:
        if value is None:
            return None

        match value["item_content"]:
            case str(raw):
                item_content: TextItem = TextItem(value=raw)
            case _:
                raise ValueError(
                    f"Unexpected ItemContent: {value['item_content']}",
                )

        return ItemSnapshot(
            item_id=UUID(value["item_id"]),
            item_content=item_content,
        )
