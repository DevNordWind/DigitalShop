from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.actor import UserActor
from app.domain.common.money import Currency
from app.domain.order.entity import Order
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService, OrderDomainService
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.item.value_object import ItemsAmount
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionWarehouseDomainService
from app.domain.shopping.position.value_object import PositionId


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
        warehouse_service: PositionWarehouseDomainService,
        order_service: OrderDomainService,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._warehouse_service = warehouse_service
        self._order_service = order_service
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: CreateOrderCmd) -> OrderId:
        items_amount = ItemsAmount(cmd.items_amount)
        actor: UserActor = OrderAccessService.ensure_can_create(
            actor=await self._actor_provider.get()
        )

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(cmd.position_id),
        )
        if not position:
            raise PositionNotFoundError

        await self._warehouse_service.check_availability(
            position=position,
            amount=items_amount,
        )

        order: Order = self._order_service.create(
            customer_id=actor.id,
            position=position,
            items_amount=items_amount,
            customer_currency=cmd.customer_currency,
        )
        order_id = order.id
        await self._order_repo.add(order)
        await self._session.commit()

        return order_id
