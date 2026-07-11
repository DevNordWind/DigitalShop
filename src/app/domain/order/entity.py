from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domain.common.money import Money
from app.domain.coupon.entity import Coupon
from app.domain.order.const import ORDER_EXPIRATION_TIME
from app.domain.order.enums import OrderStatus, PaymentSourceType
from app.domain.order.exception import (
    OrderAppliedCouponRequiredError,
    OrderAwaitingPaymentForbiddenError,
    OrderCancellationForbiddenError,
    OrderConfirmationForbiddenError,
    OrderCouponApplicationForbiddenError,
    OrderCurrencyChangeForbiddenError,
    OrderExpirationForbiddenError,
    OrderFailureForbiddenError,
    OrderFreePaymentForbiddenError,
    OrderItemsAmountChangeForbiddenError,
    OrderPaymentRequiredError,
)
from app.domain.order.value_object import (
    AppliedCoupon,
    OrderId,
    PaymentSource,
)
from app.domain.payment.value_object import PaymentId
from app.domain.shopping.position.item.value_object import ItemsAmount, ItemSnapshot
from app.domain.shopping.position.value_object import PositionSnapshot
from app.domain.user.value_object import UserId


@dataclass(kw_only=True)
class Order:
    id: OrderId
    customer_id: UserId

    sub_total: Money
    status: OrderStatus = OrderStatus.NEW
    source: PaymentSource | None = None

    position: PositionSnapshot
    items_amount: ItemsAmount
    items: tuple[ItemSnapshot, ...] | None = None

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
        return self.total == Money.zero(currency=self.total.currency)

    def apply_coupon(self, coupon: Coupon, now: datetime) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderCouponApplicationForbiddenError

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
            raise OrderConfirmationForbiddenError

        if not self.applied_coupon:
            raise OrderAppliedCouponRequiredError

        if not self.is_free:
            raise OrderPaymentRequiredError

        self.items = items
        self.confirm(now)

    def confirm_with_wallet(
        self,
        items: tuple[ItemSnapshot, ...],
        now: datetime,
    ) -> None:
        if self.is_free:
            raise OrderFreePaymentForbiddenError

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
            raise OrderAwaitingPaymentForbiddenError

        if self.is_free:
            raise OrderFreePaymentForbiddenError

        self.items = items
        self.source = PaymentSource(
            payment_id=payment_id,
            type=PaymentSourceType.PAYMENT,
        )
        self.awaited_payment_at = now
        self.status = OrderStatus.AWAITING_PAYMENT

    def confirm(self, now: datetime) -> None:
        if self.status not in (OrderStatus.NEW, OrderStatus.AWAITING_PAYMENT):
            raise OrderConfirmationForbiddenError

        self.status = OrderStatus.CONFIRMED
        self.confirmed_at = now

    def fail(self, now: datetime) -> None:
        if self.status not in {OrderStatus.AWAITING_PAYMENT, OrderStatus.NEW}:
            raise OrderFailureForbiddenError

        self.status = OrderStatus.FAILED
        self.failed_at = now

    def cancel(self, now: datetime) -> None:
        if self.status not in {OrderStatus.AWAITING_PAYMENT, OrderStatus.NEW}:
            raise OrderCancellationForbiddenError

        self.status = OrderStatus.CANCELLED
        self.cancelled_at = now

    def expire(self, now: datetime) -> None:
        if self.status not in {OrderStatus.NEW, OrderStatus.AWAITING_PAYMENT}:
            raise OrderExpirationForbiddenError

        reference_time: datetime = self.awaited_payment_at or self.created_at
        if now < reference_time + timedelta(seconds=ORDER_EXPIRATION_TIME):
            raise OrderExpirationForbiddenError

        self.status = OrderStatus.EXPIRED
        self.expired_at = now

    def change_items_amount(
        self,
        recalculated_sub_total: Money,
        new_items_amount: ItemsAmount,
    ) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderItemsAmountChangeForbiddenError

        self.sub_total = recalculated_sub_total
        self.items_amount = new_items_amount

    def change_currency(self, recalculated_sub_total: Money) -> None:
        if self.status != OrderStatus.NEW:
            raise OrderCurrencyChangeForbiddenError

        self.sub_total = recalculated_sub_total
