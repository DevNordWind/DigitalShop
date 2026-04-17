from dataclasses import dataclass
from uuid import UUID

from app.order.dto.order import OrderDTO, OrderMapper, PublicOrderDTO
from app.order.exception import OrderNotFound
from app.order.port.reader import OrderReader
from app.user.port import UserIdentifyProvider
from domain.order.exception import OrderPermissionDenied
from domain.order.service import OrderAccessService
from domain.order.value_object import OrderId
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetOrderQuery:
    id: UUID


class GetOrder:
    def __init__(self, reader: OrderReader, idp: UserIdentifyProvider):
        self._reader: OrderReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: GetOrderQuery,
    ) -> OrderDTO | PublicOrderDTO:
        order: OrderDTO | None = await self._reader.read_by_id(
            order_id=OrderId(query.id),
        )
        if not order:
            raise OrderNotFound

        viewer_role, viewer_id = (
            await self._idp.get_role(),
            await self._idp.get_user_id(),
        )

        if not OrderAccessService.can_view(
            viewer_role=viewer_role,
            viewer_id=viewer_id,
            customer_id=UserId(order.customer_id),
        ):
            raise OrderPermissionDenied

        if not OrderAccessService.can_view_items(
            viewer_role=viewer_role,
            viewer_id=viewer_id,
            customer_id=UserId(order.customer_id),
            order_status=order.status,
        ):
            return OrderMapper.to_public(src=order)

        return order
