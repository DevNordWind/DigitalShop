import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.exception import DataCorruptionError
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.referral.cmd import (
    CreateReferralAwardFromOrder,
    CreateReferralAwardFromOrderCmd,
)
from app.domain.common.money import Money
from app.domain.common.port import Clock
from app.domain.coupon.entity import CouponRedemption
from app.domain.coupon.port import CouponRedemptionRepository
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId
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
    SellContext,
)
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class PayOrderWithWalletCmd:
    order_id: UUID


class PayOrderWithWallet:
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        redemption_repo: CouponRedemptionRepository,
        fulfillment_service: PositionFulfillmentDomainService,
        session: DatabaseSession,
        wallet_repo: WalletRepository,
        actor_provider: ActorProvider,
        clock: Clock,
        create_award: CreateReferralAwardFromOrder,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._redemption_repo = redemption_repo
        self._fulfillment_service = fulfillment_service
        self._session = session
        self._actor_provider = actor_provider
        self._wallet_repo = wallet_repo
        self._clock = clock
        self._create_award = create_award

    async def __call__(self, cmd: PayOrderWithWalletCmd) -> None:
        order: Order | None = await self._order_repo.acquire(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFoundError

        OrderAccessService.ensure_can_checkout(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )

        total: Money = order.total
        now: datetime = self._clock.now()

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
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

        wallet: Wallet | None = await self._wallet_repo.acquire_user_id_by_currency(
            user_id=order.customer_id,
            currency=total.currency,
        )
        if not wallet:
            raise DataCorruptionError(
                f"User {order.customer_id} exists but its wallet was not found",
            )

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError

            redemption.confirm(now=now)

        wallet.withdraw(amount=total)
        await self._fulfillment_service.sell(
            position=position, snapshots=items, ctx=SellContext(now=now)
        )
        order.confirm_with_wallet(now=now, items=items)

        await self._session.commit()

        try:
            await self._create_award(
                CreateReferralAwardFromOrderCmd(order_id=cmd.order_id),
            )
        except Exception as e:
            logger.error(e)
