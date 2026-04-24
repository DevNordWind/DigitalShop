from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.order.exception import OrderNotFound
from domain.common.money import Currency
from domain.common.port import Clock
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderService
from domain.order.value_object import OrderId


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
        service: OrderService,
    ):
        self._order_repo: OrderRepository = order_repo
        self._service: OrderService = service
        self._session: DatabaseSession = session
        self._clock: Clock = clock

    async def __call__(self, cmd: ChangeOrderCurrencyCmd) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFound

        self._service.change_currency(
            order=order,
            new_customer_currency=cmd.new_currency,
        )

        await self._session.commit()
