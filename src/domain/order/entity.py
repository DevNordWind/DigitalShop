from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Final

from domain.common.money import Money
from domain.coupon.entity import Coupon
from domain.order.enums import OrderStatus, PaymentSourceType
from domain.order.exception import (
    OrderAwaitingPaymentForbidden,
    OrderCancellationForbidden,
    OrderConfirmationForbidden,
    OrderCouponApplicationForbidden,
    OrderCurrencyChangeForbidden,
    OrderExpirationForbidden,
    OrderFailureForbidden,
    OrderFreePaymentForbidden,
    OrderItemsAmountChangeForbidden,
    OrderPaymentRequired,
)
from domain.order.value_object import (
    AppliedCoupon,
    ItemSnapshot,
    OrderId,
    PositionSnapshot,
)
from domain.order.value_object.source import PaymentSource
from domain.payment.value_object import PaymentId
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.user.value_object import UserId

ORDER_TTL_SECONDS: Final[int] = 900


@dataclass(kw_only=True)
class Order:
    id: OrderId
    customer_id: UserId

    sub_total: Money
    status: OrderStatus = OrderStatus.NEW
    source: PaymentSource | None = None

    position: PositionSnapshot
    items: tuple[ItemSnapshot, ...] | None = None
    items_amount: ItemsAmount

    created_at: datetime
    awaited_payment_at: datetime | None = None
    failed_at: datetime | None = None
    confirmed_at: datetime | None = None
    cancelled_at: datetime | None = None
    expired_at: datetime | None = None

    applied_coupon: AppliedCoupon | None = None

    @property
    def total(self) -> Money:
        if not self.applied_coupon:
            return self.sub_total

        return self.sub_total - self.applied_coupon.discount

    @property
    def is_free(self) -> bool:
        return self.total.amount == Decimal("0.00")

    def apply_coupon(self, coupon: Coupon, now: datetime) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderCouponApplicationForbidden

        self.applied_coupon = AppliedCoupon(
            discount=coupon.calculate_discount(
                sub_total=self.sub_total,
                now=now,
            ),
            coupon_id=coupon.id,
        )

    def confirm_with_discount(
        self, items: tuple[ItemSnapshot, ...], now: datetime
    ) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderConfirmationForbidden

        if not self.is_free:
            raise OrderPaymentRequired

        self.items = items
        self.confirm(now)

    def confirm_with_wallet(
        self,
        items: tuple[ItemSnapshot, ...],
        now: datetime,
    ) -> None:
        if self.is_free:
            raise OrderFreePaymentForbidden

        self.items = items
        self.source = PaymentSource(
            payment_id=None,
            type=PaymentSourceType.WALLET,
        )
        self.confirm(now)

    def await_payment(
        self,
        items: tuple[ItemSnapshot, ...],
        payment_id: PaymentId,
        now: datetime,
    ) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderAwaitingPaymentForbidden

        if self.is_free:
            raise OrderFreePaymentForbidden

        self.items = items
        self.source = PaymentSource(
            payment_id=payment_id,
            type=PaymentSourceType.PAYMENT,
        )
        self.awaited_payment_at = now
        self.status = OrderStatus.AWAITING_PAYMENT

    def confirm(self, now: datetime) -> None:
        if self.status not in (OrderStatus.NEW, OrderStatus.AWAITING_PAYMENT):
            raise OrderConfirmationForbidden

        self.status = OrderStatus.CONFIRMED
        self.confirmed_at = now

    def fail(self, now: datetime) -> None:
        if self.status not in {OrderStatus.AWAITING_PAYMENT, OrderStatus.NEW}:
            raise OrderFailureForbidden

        self.status = OrderStatus.FAILED
        self.failed_at = now

    def cancel(self, now: datetime) -> None:
        if self.status not in {OrderStatus.AWAITING_PAYMENT, OrderStatus.NEW}:
            raise OrderCancellationForbidden

        self.status = OrderStatus.CANCELLED
        self.cancelled_at = now

    def expire(self, now: datetime) -> None:
        if self.status not in {OrderStatus.NEW, OrderStatus.AWAITING_PAYMENT}:
            raise OrderExpirationForbidden

        reference_time: datetime = self.awaited_payment_at or self.created_at
        if now < reference_time + timedelta(seconds=ORDER_TTL_SECONDS):
            raise OrderExpirationForbidden

        self.status = OrderStatus.EXPIRED
        self.expired_at = now

    def change_items_amount(
        self,
        recalculated_sub_total: Money,
        new_items_amount: ItemsAmount,
    ) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderItemsAmountChangeForbidden

        self.sub_total = recalculated_sub_total
        self.items_amount = new_items_amount

    def change_currency(self, recalculated_sub_total: Money) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderCurrencyChangeForbidden

        self.sub_total = recalculated_sub_total
