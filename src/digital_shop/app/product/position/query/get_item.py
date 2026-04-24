from dataclasses import dataclass
from uuid import UUID

from app.product.position.dto.item import ItemDTO
from app.product.position.exception import (
    PositionItemNotFound,
)
from app.product.position.port import PositionReader
from app.user.port import UserIdentifyProvider
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.value_object import ItemId
from domain.product.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class GetPositionItemQuery:
    id: UUID


class GetPositionItem:
    def __init__(
        self,
        reader: PositionReader,
        idp: UserIdentifyProvider,
    ):
        self._reader: PositionReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: GetPositionItemQuery) -> ItemDTO:
        if not PositionAccessService.can_view_item(
            viewer_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        item: ItemDTO | None = await self._reader.read_item(
            item_id=ItemId(query.id),
        )
        if not item:
            raise PositionItemNotFound

        return item
