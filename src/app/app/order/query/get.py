from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.order.dto.order import OrderDTO, OrderMapper, PublicOrderDTO
from app.app.order.port import OrderReader
from app.domain.common.actor import Actor
from app.domain.order.enums import OrderAccessLevel
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetOrderQuery:
    id: UUID


class GetOrder:
    def __init__(self, reader: OrderReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: GetOrderQuery,
    ) -> OrderDTO | PublicOrderDTO:
        order: OrderDTO | None = await self._reader.read_by_id(
            order_id=OrderId(query.id),
        )
        if not order:
            raise OrderNotFoundError

        actor: Actor = await self._actor_provider.get()
        customer_id: UserId = UserId(order.customer_id)

        OrderAccessService.ensure_can_view(actor=actor, customer_id=customer_id)
        access_level: OrderAccessLevel = OrderAccessService.determine_access_level(
            actor=actor, customer_id=customer_id, order_status=order.status
        )
        if access_level == OrderAccessLevel.PREVIEW:
            return OrderMapper.to_public(src=order)

        return order
