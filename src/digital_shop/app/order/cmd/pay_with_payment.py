import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from app.common.dto.money import MoneyMapper
from app.common.port import DatabaseSession
from app.order.exception import OrderNotFound
from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.payment.port.payment import CreateInvoice, Invoice
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.money import Money
from domain.common.port import Clock
from domain.order.entity import ORDER_TTL_SECONDS, Order
from domain.order.exception import OrderPermissionDenied
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderAccessService
from domain.order.value_object import ItemSnapshot, OrderId
from domain.payment.entity import Payment
from domain.payment.enums import PaymentMethod, PaymentPurposeType
from domain.payment.port import (
    PaymentCommissionRuleRepository,
    PaymentRepository,
)
from domain.payment.rule import PaymentCommissionRule
from domain.payment.service import PaymentService
from domain.payment.value_object import PaymentExternalId, PaymentPurpose
from domain.product.position.entity import Position
from domain.product.position.exception import OutOfStock
from domain.product.position.item.entity import Item
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.product.position.value_object import PositionId
from domain.user.entity import User

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class PayOrderWithPaymentCmd:
    order_id: UUID
    method: PaymentMethod


class PayOrderWithPayment:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        current_user: GetCurrentUser,
        payment_repo: PaymentRepository,
        rule_repo: PaymentCommissionRuleRepository,
        payment_factory: PaymentMethodGatewayFactory,
        payment_service: PaymentService,
        warehouse_service: PositionWarehouseService,
        position_repo: PositionRepository,
        clock: Clock,
    ):
        self._order_repo: OrderRepository = order_repo
        self._session: DatabaseSession = session
        self._payment_service: PaymentService = payment_service
        self._payment_repo: PaymentRepository = payment_repo
        self._rule_repo: PaymentCommissionRuleRepository = rule_repo
        self._current_user: GetCurrentUser = current_user
        self._payment_factory: PaymentMethodGatewayFactory = payment_factory
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._position_repo: PositionRepository = position_repo
        self._clock: Clock = clock

    async def __call__(self, cmd: PayOrderWithPaymentCmd) -> Invoice:
        customer: User = await self._current_user()
        order: Order | None = await self._order_repo.get_for_update(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFound

        if not OrderAccessService.can_checkout(
            actor_id=customer.id, order_customer_id=order.customer_id
        ):
            raise OrderPermissionDenied

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        now: datetime = self._clock.now()
        if not position:
            order.cancel(now)
            await self._session.commit()
            raise PositionNotFound

        try:
            items: list[
                Item
            ] = await self._warehouse_service.acquire_for_reserve(
                position=position,
                amount=order.items_amount,
            )
        except OutOfStock as e:
            if e.available == 0:
                order.cancel(now)
                await self._session.commit()

            raise

        total: Money = order.total
        rule: PaymentCommissionRule = await self._rule_repo.get(
            method=cmd.method,
        )

        payment: Payment = self._payment_service.create(
            creator=customer,
            purpose=PaymentPurpose(
                reference_id=order.id.value,
                type=PaymentPurposeType.ORDER_PAYMENT,
            ),
            amount=total,
            commission_rule=rule,
            method=cmd.method,
        )
        await self._payment_repo.add(payment)
        await self._session.flush()
        gw: PaymentMethodGateway = await self._payment_factory.get(
            payment.method,
        )
        try:
            invoice: Invoice = await gw.create(
                data=CreateInvoice(
                    payment_id=payment.id.value,
                    to_pay=MoneyMapper.to_dto(src=payment.to_pay),
                    expires_in=timedelta(seconds=ORDER_TTL_SECONDS),
                ),
            )

            payment.start(
                external_id=PaymentExternalId(invoice.invoice_id),
                now=now,
            )

        except PaymentMethodGatewayError as e:
            logger.exception(f"PaymentMethodGatewayError: {e}")
            order.fail(
                now=now,
            )
            payment.fail(now=now)
            await self._session.commit()
            raise

        order.await_payment(
            payment_id=payment.id,
            items=tuple(
                ItemSnapshot(item_id=item.id.value, item_content=item.content)
                for item in items
            ),
            now=now,
        )

        await self._session.commit()

        return invoice
