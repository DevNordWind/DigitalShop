from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.exception import (
    PositionItemNotFound,
)
from app.user.port import UserIdentifyProvider
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class DeletePositionItemCmd:
    item_id: UUID


class DeletePositionItem:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: PositionRepository = repo
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: DeletePositionItemCmd) -> None:
        if not PositionAccessService.can_delete_item(
            deleter_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        item: Item | None = await self._repo.get_item_for_update(
            item_id=ItemId(cmd.item_id),
        )
        if not item:
            raise PositionItemNotFound

        item.ensure_can_delete()

        await self._repo.delete_item(item)
        await self._session.commit()
