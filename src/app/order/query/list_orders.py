from dataclasses import dataclass
from uuid import UUID

from app.common.dto.query_params import OffsetPaginationParams
from app.order.dto.order import OrderDTO, OrderMapper, PublicOrderDTO
from app.order.dto.paginated import OrdersPaginated, OrdersPaginatedByReader
from app.order.dto.sorting import OrderSortingParams
from app.order.port.reader import OrderReader
from app.user.port import UserIdentifyProvider
from domain.order.enums import OrderStatus
from domain.order.exception import OrderPermissionDenied
from domain.order.service import OrderAccessService
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class ListOrdersQuery:
    customer_id: UUID
    sorting: OrderSortingParams
    pagination: OffsetPaginationParams
    status: OrderStatus | None


class ListOrders:
    def __init__(self, reader: OrderReader, idp: UserIdentifyProvider):
        self._reader: OrderReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: ListOrdersQuery) -> OrdersPaginated:
        viewer_role, viewer_id = (
            await self._idp.get_role(),
            await self._idp.get_user_id(),
        )

        if not OrderAccessService.can_view(
            viewer_role=viewer_role,
            viewer_id=viewer_id,
            customer_id=UserId(query.customer_id),
        ):
            raise OrderPermissionDenied

        paginated: OrdersPaginatedByReader = (
            await self._reader.read_by_customer_id(
                customer_id=UserId(query.customer_id),
                sorting=query.sorting,
                pagination=query.pagination,
                status=query.status,
            )
        )

        orders: list[OrderDTO | PublicOrderDTO] = [
            OrderMapper.to_public(src=order)
            if not OrderAccessService.can_view_items(
                viewer_role=viewer_role,
                viewer_id=viewer_id,
                customer_id=UserId(order.customer_id),
                order_status=order.status,
            )
            else order
            for order in paginated.orders
        ]

        return OrdersPaginated(orders=orders, total=paginated.total)
