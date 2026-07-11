import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.exception import DataCorruptionError
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.payment.service import PaymentApplicationService
from app.app.payment.service.service import CancelPaymentData
from app.domain.common.port import Clock
from app.domain.coupon.entity import CouponRedemption
from app.domain.coupon.port import CouponRedemptionRepository
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service.fulfillment import (
    PositionFulfillmentDomainService,
)
from app.domain.shopping.position.value_object import PositionId

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class CancelOrderCmd:
    id: UUID


class CancelOrder:
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        payment_service: PaymentApplicationService,
        redemption_repo: CouponRedemptionRepository,
        fulfilment_service: PositionFulfillmentDomainService,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._payment_service = payment_service
        self._redemption_repo = redemption_repo
        self._fulfilment_service = fulfilment_service
        self._session = session
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: CancelOrderCmd) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.id),
        )
        if not order:
            raise OrderNotFoundError

        OrderAccessService.ensure_can_cancel(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )
        now: datetime = self._clock.now()
        order.cancel(now=now)

        if order.source and order.source.payment_id is not None:
            await self._payment_service.cancel(
                data=CancelPaymentData(id=order.source.payment_id.value)
            )

        if order.items:
            position: Position | None = await self._position_repo.get(
                position_id=PositionId(order.position.position_id)
            )
            if not position:
                logger.warning("Position %s was deleted", cmd.id.hex)
            else:
                await self._fulfilment_service.rollback(
                    position=position, snapshots=order.items
                )

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError(
                    "Order exists with applied coupon without CouponRedemption"
                )

            redemption.cancel(now=now)

        await self._session.commit()
