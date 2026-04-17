import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession
from app.order.exception import OrderNotFound
from app.product.position.exception import PositionNotFound
from app.referral.cmd import (
    CreateReferralAwardFromOrder,
    CreateReferralAwardFromOrderCmd,
)
from app.user.service import GetCurrentUser
from domain.common.money import Money
from domain.common.port import Clock
from domain.coupon.entity import CouponRedemption
from domain.coupon.port import CouponRedemptionRepository
from domain.order.entity import Order
from domain.order.exception import OrderPermissionDenied
from domain.order.port.repository import OrderRepository
from domain.order.service import OrderAccessService
from domain.order.value_object import ItemSnapshot, OrderId
from domain.product.position.entity import Position
from domain.product.position.exception import OutOfStock
from domain.product.position.item.entity import Item
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.product.position.value_object import PositionId
from domain.user.entity import User
from domain.wallet.entity import Wallet
from domain.wallet.port import WalletRepository

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
        warehouse_service: PositionWarehouseService,
        session: DatabaseSession,
        wallet_repo: WalletRepository,
        current_user: GetCurrentUser,
        clock: Clock,
        create_award: CreateReferralAwardFromOrder,
    ):
        self._position_repo: PositionRepository = position_repo
        self._order_repo: OrderRepository = order_repo
        self._redemption_repo: CouponRedemptionRepository = redemption_repo
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._wallet_repo: WalletRepository = wallet_repo
        self._clock: Clock = clock
        self._create_award: CreateReferralAwardFromOrder = create_award

    async def __call__(self, cmd: PayOrderWithWalletCmd) -> None:
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

        total: Money = order.total
        now: datetime = self._clock.now()

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        if not position:
            order.cancel(now)
            await self._session.commit()
            raise PositionNotFound

        try:
            items: list[Item] = await self._warehouse_service.acquire_for_sell(
                position=position,
                amount=order.items_amount,
            )
        except OutOfStock as e:
            if e.available == 0:
                order.cancel(now)
                await self._session.commit()

            raise

        wallet: (
            Wallet | None
        ) = await self._wallet_repo.get_by_currency_for_update(
            user_id=order.customer_id,
            currency=total.currency,
        )
        if not wallet:
            raise DataCorruptionError(
                f"User {order.customer_id} exists but its wallet was not found",  # noqa: E501
            )

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError

            redemption.confirm(now=now)

        wallet.withdraw(amount=total)
        order.confirm_with_wallet(
            now=now,
            items=tuple(
                ItemSnapshot(item_id=item.id.value, item_content=item.content)
                for item in items
            ),
        )

        await self._session.commit()

        try:
            await self._create_award(
                CreateReferralAwardFromOrderCmd(order_id=cmd.order_id),
            )
        except Exception as e:
            logger.error(e)
