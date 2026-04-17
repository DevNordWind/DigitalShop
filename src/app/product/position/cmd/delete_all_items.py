from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.user.port import UserIdentifyProvider
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.enums import ItemStatus
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class DeleteAllPositionItemsCmd:
    position_id: UUID


class DeleteAllPositionItems:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: PositionRepository = repo
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: DeleteAllPositionItemsCmd) -> None:
        if not PositionAccessService.can_delete_item(
            deleter_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        items: list[Item] = await self._repo.get_items_for_update(
            position_id=PositionId(cmd.position_id),
            status=ItemStatus.ARCHIVED,
        )

        for item in items:
            item.ensure_can_delete()
            await self._repo.delete_item(item)

        await self._session.commit()
