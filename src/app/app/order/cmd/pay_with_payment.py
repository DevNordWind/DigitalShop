from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.payment.port.payment import Invoice
from app.app.payment.service import (
    CreatedPayment,
    CreatePaymentData,
    FailedCreatedPayment,
    PaymentApplicationService,
)
from app.domain.common.actor import UserActor
from app.domain.common.money import Money
from app.domain.common.port import Clock
from app.domain.order.const import ORDER_EXPIRATION_TIME
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId
from app.domain.payment.enums import PaymentMethod, PaymentPurposeType
from app.domain.payment.port import PaymentCommissionRuleRepository, PaymentRepository
from app.domain.payment.value_object import PaymentPurpose
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import (
    OutOfStockError,
    PositionNotFoundError,
)
from app.domain.shopping.position.item.value_object import ItemSnapshot
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service.fulfillment import (
    PositionFulfillmentDomainService,
)
from app.domain.shopping.position.value_object import (
    HoldContext,
    PositionId,
)


@dataclass(slots=True, frozen=True)
class PayOrderWithPaymentCmd:
    order_id: UUID
    method: PaymentMethod


class PayOrderWithPayment:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        payment_repo: PaymentRepository,
        rule_repo: PaymentCommissionRuleRepository,
        payment_service: PaymentApplicationService,
        fulfillment_service: PositionFulfillmentDomainService,
        position_repo: PositionRepository,
        clock: Clock,
    ):
        self._order_repo = order_repo
        self._session = session
        self._payment_service = payment_service
        self._payment_repo = payment_repo
        self._rule_repo = rule_repo
        self._actor_provider = actor_provider
        self._fulfillment_service = fulfillment_service
        self._position_repo = position_repo
        self._clock = clock

    async def __call__(self, cmd: PayOrderWithPaymentCmd) -> Invoice:
        order: Order | None = await self._order_repo.acquire(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFoundError

        actor: UserActor = OrderAccessService.ensure_can_checkout(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        now: datetime = self._clock.now()
        if not position:
            order.cancel(now)
            await self._session.commit()
            raise PositionNotFoundError

        try:
            items: tuple[ItemSnapshot, ...] = await self._fulfillment_service.hold(
                position=position, ctx=HoldContext(now=now, amount=order.items_amount)
            )
        except OutOfStockError as e:
            if e.available == 0:
                order.cancel(now)
                await self._session.commit()

            raise

        total: Money = order.total

        created_payment: CreatedPayment = await self._payment_service.create(
            data=CreatePaymentData(
                actor=actor,
                purpose=PaymentPurpose(
                    reference_id=order.id.value, type=PaymentPurposeType.ORDER_PAYMENT
                ),
                method=cmd.method,
                amount=total,
                expires_in=timedelta(seconds=ORDER_EXPIRATION_TIME),
            )
        )
        if isinstance(created_payment, FailedCreatedPayment):
            order.fail(now=now)
            await self._session.commit()
            raise created_payment.e

        order.await_payment(items=items, payment_id=created_payment.payment.id, now=now)
        await self._session.commit()

        return created_payment.invoice
