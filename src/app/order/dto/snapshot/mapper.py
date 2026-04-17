from app.common.dto.localized import LocalizedTextMapper
from app.order.dto.snapshot.snapshot import (
    ItemSnapshotDTO,
    PositionSnapshotDTO,
)
from app.product.position.dto.item_content import ItemContentMapper
from app.product.position.dto.price import PositionPriceMapper
from domain.order.value_object import ItemSnapshot, PositionSnapshot


class ItemSnapshotMapper:
    @classmethod
    def to_dto(cls, src: ItemSnapshot) -> ItemSnapshotDTO:
        return ItemSnapshotDTO(
            item_id=src.item_id,
            item_content=ItemContentMapper.to_dto(src=src.item_content),
        )


class PositionSnapshotMapper:
    @classmethod
    def to_dto(cls, src: PositionSnapshot) -> PositionSnapshotDTO:
        return PositionSnapshotDTO(
            category_id=src.category_id,
            position_id=src.position_id,
            position_name=LocalizedTextMapper.to_dto(src=src.position_name),
            price=PositionPriceMapper.to_dto(src=src.price),
        )
