import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession
from app.order.exception import OrderNotFound
from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.payment.port.payment import CancelInvoice
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.coupon.entity import CouponRedemption
from domain.coupon.port import CouponRedemptionRepository
from domain.order.entity import Order
from domain.order.exception import OrderPermissionDenied
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderAccessService
from domain.order.value_object import OrderId
from domain.payment.entity import Payment
from domain.payment.port import PaymentRepository
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.user.entity import User

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class CancelOrderCmd:
    id: UUID


class CancelOrder:
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        payment_repo: PaymentRepository,
        redemption_repo: CouponRedemptionRepository,
        payment_factory: PaymentMethodGatewayFactory,
        warehouse_service: PositionWarehouseService,
        session: DatabaseSession,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._position_repo: PositionRepository = position_repo
        self._order_repo: OrderRepository = order_repo
        self._payment_repo: PaymentRepository = payment_repo
        self._redemption_repo: CouponRedemptionRepository = redemption_repo
        self._payment_factory: PaymentMethodGatewayFactory = payment_factory
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(self, cmd: CancelOrderCmd) -> None:
        current_user: User = await self._current_user()
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFound

        if not OrderAccessService.can_cancel(
            actor_id=current_user.id,
            actor_role=current_user.role,
            order_customer_id=order.customer_id,
        ):
            raise OrderPermissionDenied

        now: datetime = self._clock.now()

        order.cancel(now=now)

        if order.source and order.source.payment_id is not None:
            payment: Payment | None = await self._payment_repo.get(
                payment_id=order.source.payment_id,
            )
            if not payment:
                raise DataCorruptionError(
                    f"Order {order.id} exists but it's payment was not found",
                )
            payment.cancel(now=now)
            if payment.external_id:
                gateway: PaymentMethodGateway = (
                    await self._payment_factory.get(method=payment.method)
                )
                try:
                    await gateway.cancel(
                        data=CancelInvoice(
                            invoice_id=payment.external_id.value,
                        ),
                    )
                except PaymentMethodGatewayError as e:
                    logger.error(e)

        if order.items:
            items_ids: set[ItemId] = {
                ItemId(item.item_id) for item in order.items
            }
            await self._warehouse_service.release_reserved(
                items_ids=list(items_ids),
            )

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError

            redemption.cancel(now=now)

        await self._session.commit()
