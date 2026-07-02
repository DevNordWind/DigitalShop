from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderDomainService
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.item.value_object import ItemsAmount
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionWarehouseDomainService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ChangeOrderItemsAmountCmd:
    id: UUID
    new_items_amount: int


class ChangeOrderItemsAmount:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        warehouse_service: PositionWarehouseDomainService,
        position_repo: PositionRepository,
        clock: Clock,
        service: OrderDomainService,
    ):
        self._warehouse_service = warehouse_service
        self._order_repo = order_repo
        self._service = service
        self._session = session
        self._clock = clock
        self._position_repo = position_repo

    async def __call__(self, cmd: ChangeOrderItemsAmountCmd) -> None:
        items_amount = ItemsAmount(cmd.new_items_amount)

        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFoundError

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        if not position:
            order.cancel(self._clock.now())
            await self._session.commit()
            raise PositionNotFoundError

        await self._warehouse_service.check_availability(
            position=position,
            amount=items_amount,
        )

        self._service.change_items_amount(
            order=order,
            new_items_amount=items_amount,
        )

        await self._session.commit()
