from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.money import Currency
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderService
from domain.order.value_object import OrderId
from domain.product.position.entity import Position
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class CreateOrderCmd:
    position_id: UUID
    items_amount: int

    customer_currency: Currency


class CreateOrder:
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        warehouse_service: PositionWarehouseService,
        order_service: OrderService,
        session: DatabaseSession,
        current_user: GetCurrentUser,
    ):
        self._position_repo: PositionRepository = position_repo
        self._order_repo: OrderRepository = order_repo
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._order_service: OrderService = order_service
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user

    async def __call__(self, cmd: CreateOrderCmd) -> OrderId:
        items_amount = ItemsAmount(cmd.items_amount)
        customer: User = await self._current_user()

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(cmd.position_id),
        )
        if not position:
            raise PositionNotFound

        await self._warehouse_service.check_availability(
            position=position,
            amount=items_amount,
        )

        order: Order = self._order_service.create(
            customer=customer,
            position=position,
            items_amount=items_amount,
            customer_currency=cmd.customer_currency,
        )
        order_id = order.id
        await self._order_repo.add(order)
        await self._session.commit()

        return order_id
