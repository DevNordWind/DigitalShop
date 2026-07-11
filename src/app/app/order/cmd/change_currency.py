from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.money import Currency
from app.domain.common.port import Clock
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService, OrderDomainService
from app.domain.order.value_object import OrderId


@dataclass(slots=True, frozen=True)
class ChangeOrderCurrencyCmd:
    id: UUID
    new_currency: Currency


class ChangeOrderCurrency:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        clock: Clock,
        actor_provider: ActorProvider,
        service: OrderDomainService,
    ):
        self._order_repo = order_repo
        self._service = service
        self._session = session
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: ChangeOrderCurrencyCmd) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFoundError

        OrderAccessService.ensure_can_change_currency(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )

        self._service.change_currency(
            order=order,
            new_customer_currency=cmd.new_currency,
        )

        await self._session.commit()
