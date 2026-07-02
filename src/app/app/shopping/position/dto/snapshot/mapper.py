from app.app.common.dto.localized import LocalizedTextMapper
from app.app.shopping.position.dto.item_content import ItemContentMapper
from app.app.shopping.position.dto.price import PositionPriceMapper
from app.app.shopping.position.dto.snapshot.snapshot import (
    ItemSnapshotDTO,
    PositionSnapshotDTO,
)
from app.domain.shopping.position.item.value_object import ItemSnapshot
from app.domain.shopping.position.value_object import PositionSnapshot


class ItemSnapshotMapper:
    @classmethod
    def to_dto(cls, src: ItemSnapshot) -> ItemSnapshotDTO:
        return ItemSnapshotDTO(
            id=src.id, content=ItemContentMapper.to_dto(src=src.content)
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
