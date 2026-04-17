from dataclasses import dataclass
from uuid import UUID

from app.product.position.dto.position import PositionDTO
from app.product.position.exception import PositionNotFound
from app.product.position.port import PositionReader
from app.user.port import UserIdentifyProvider
from domain.product.position.enums import PositionStatus
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class GetPositionQuery:
    id: UUID


class GetPosition:
    def __init__(self, reader: PositionReader, idp: UserIdentifyProvider):
        self._reader: PositionReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: GetPositionQuery) -> PositionDTO:
        position: PositionDTO | None = await self._reader.read(
            position_id=PositionId(query.id),
        )
        if not position:
            raise PositionNotFound

        if (
            position.status == PositionStatus.ARCHIVED
            and not PositionAccessService.can_view_archived(
                viewer_role=await self._idp.get_role(),
            )
        ):
            raise PositionPermissionDenied

        return position
