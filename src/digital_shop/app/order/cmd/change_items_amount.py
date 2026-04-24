from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.order.exception import OrderNotFound
from app.product.position.exception import PositionNotFound
from domain.common.port import Clock
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderService
from domain.order.value_object import OrderId
from domain.product.position.entity import Position
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.product.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ChangeOrderItemsAmountCmd:
    id: UUID
    new_items_amount: int


class ChangeOrderItemsAmount:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        warehouse_service: PositionWarehouseService,
        position_repo: PositionRepository,
        clock: Clock,
        service: OrderService,
    ):
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._order_repo: OrderRepository = order_repo
        self._service: OrderService = service
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._position_repo: PositionRepository = position_repo

    async def __call__(self, cmd: ChangeOrderItemsAmountCmd) -> None:
        items_amount = ItemsAmount(cmd.new_items_amount)

        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFound

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        if not position:
            order.cancel(self._clock.now())
            await self._session.commit()
            raise PositionNotFound

        await self._warehouse_service.check_availability(
            position=position,
            amount=items_amount,
        )

        self._service.change_items_amount(
            order=order,
            new_items_amount=items_amount,
        )

        await self._session.commit()
