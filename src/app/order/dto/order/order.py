from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.dto.money import MoneyDTO
from app.coupon.dto.coupon import CouponDTO
from app.order.dto.applied_coupon import AppliedCouponDTO
from app.order.dto.snapshot import ItemSnapshotDTO, PositionSnapshotDTO
from app.order.dto.source import PaymentSourceDTO
from domain.order.enums import OrderStatus


@dataclass(slots=True, frozen=True)
class OrderDTO:
    id: UUID
    customer_id: UUID

    sub_total: MoneyDTO
    total: MoneyDTO

    status: OrderStatus
    source: PaymentSourceDTO | None
    position: PositionSnapshotDTO
    items: tuple[ItemSnapshotDTO, ...] | None
    items_amount: int

    created_at: datetime
    awaited_payment_at: datetime | None
    failed_at: datetime | None
    confirmed_at: datetime | None
    cancelled_at: datetime | None

    applied_coupon: AppliedCouponDTO | None
    coupon: CouponDTO | None


@dataclass(slots=True, frozen=True)
class PublicOrderDTO:
    id: UUID
    customer_id: UUID

    sub_total: MoneyDTO
    total: MoneyDTO

    status: OrderStatus
    source: PaymentSourceDTO | None
    position: PositionSnapshotDTO
    items_amount: int

    created_at: datetime

    awaited_payment_at: datetime | None
    failed_at: datetime | None
    confirmed_at: datetime | None
    cancelled_at: datetime | None

    applied_coupon: AppliedCouponDTO | None
    coupon: CouponDTO | None
