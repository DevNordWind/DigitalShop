from dataclasses import dataclass
from uuid import UUID

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession, FileStorageSession
from app.product.position.dto.item_content import (
    ItemRawDTO,
    ItemRawMapper,
)
from app.product.position.exception import (
    PositionItemNotFound,
)
from app.user.port import UserIdentifyProvider
from domain.common.port import Clock
from domain.product.category.value_object import CategoryId
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.factory import ItemContentFactory
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class ReplacePositionItemCmd:
    item_id: UUID
    new_item_raw: ItemRawDTO


class ReplacePositionItem:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        file_session: FileStorageSession,
        content_factory: ItemContentFactory,
        clock: Clock,
        idp: UserIdentifyProvider,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._file_session: FileStorageSession = file_session
        self._idp: UserIdentifyProvider = idp
        self._content_factory: ItemContentFactory = content_factory
        self._clock: Clock = clock

    async def __call__(self, cmd: ReplacePositionItemCmd) -> None:
        if not PositionAccessService.can_replace_item(
            replacer_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        item: Item | None = await self._repository.get_item_for_update(
            item_id=ItemId(cmd.item_id),
        )
        if not item:
            raise PositionItemNotFound

        category_id: (
            CategoryId | None
        ) = await self._repository.get_item_category_id(item_id=item.id)
        if category_id is None:
            raise DataCorruptionError(
                f"Item {item.id} exists but its category was not found",
            )

        new_content = self._content_factory.create(
            raw=ItemRawMapper.to_value_object(src=cmd.new_item_raw),
        )

        item.replace_content(new_content=new_content, now=self._clock.now())
        await self._session.commit()
