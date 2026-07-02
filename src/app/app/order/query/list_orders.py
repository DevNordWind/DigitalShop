from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.order.dto.order import OrderDTO, OrderMapper, PublicOrderDTO
from app.app.order.dto.paginated import OrdersPaginated, OrdersPaginatedByReader
from app.app.order.dto.sorting import OrderSortingParams
from app.app.order.port import OrderReader
from app.domain.common.actor import Actor
from app.domain.order.enums import OrderAccessLevel, OrderStatus
from app.domain.order.service import OrderAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class ListOrdersQuery:
    customer_id: UUID
    sorting: OrderSortingParams
    pagination: OffsetPaginationParams
    status: OrderStatus | None


class ListOrders:
    def __init__(self, reader: OrderReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(self, query: ListOrdersQuery) -> OrdersPaginated:
        actor: Actor = await self._actor_provider.get()
        customer_id: UserId = UserId(query.customer_id)

        OrderAccessService.ensure_can_view(actor=actor, customer_id=customer_id)

        paginated: OrdersPaginatedByReader = await self._reader.read_by_customer_id(
            customer_id=customer_id,
            sorting=query.sorting,
            pagination=query.pagination,
            status=query.status,
        )

        orders: list[OrderDTO | PublicOrderDTO] = []
        for order in paginated.orders:
            level: OrderAccessLevel = OrderAccessService.determine_access_level(
                actor=actor, customer_id=customer_id, order_status=order.status
            )
            if level == OrderAccessLevel.PREVIEW:
                orders.append(OrderMapper.to_public(src=order))
            else:
                orders.append(order)

        return OrdersPaginated(orders=orders, total=paginated.total)
