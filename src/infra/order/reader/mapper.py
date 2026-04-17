from typing import Any

from app.common.dto.money import MoneyDTO
from app.coupon.dto.coupon import CouponDTO
from app.coupon.dto.discount import DiscountMapper
from app.order.dto.applied_coupon import AppliedCouponDTO
from app.order.dto.order import OrderDTO
from app.order.dto.snapshot import ItemSnapshotMapper, PositionSnapshotMapper
from app.order.dto.source import PaymentSourceDTO


class OrderReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> OrderDTO:
        return OrderDTO(
            id=row.id,
            customer_id=row.customer_id,
            sub_total=MoneyDTO(
                amount=row.sub_total_amount,
                currency=row.sub_total_currency,
            ),
            total=MoneyDTO(
                amount=row.total_amount,
                currency=row.total_currency,
            ),
            status=row.status,
            source=cls._map_source(row=row),
            items=tuple(
                [ItemSnapshotMapper.to_dto(src=item) for item in row.items],
            )
            if row.items is not None
            else None,
            created_at=row.created_at,
            confirmed_at=row.confirmed_at,
            cancelled_at=row.cancelled_at,
            applied_coupon=cls._map_applied_coupon(row=row),
            position=PositionSnapshotMapper.to_dto(src=row.position),
            items_amount=row.items_amount,
            failed_at=row.failed_at,
            coupon=cls._map_coupon(row=row),
            awaited_payment_at=row.awaited_payment_at,
        )

    @classmethod
    def _map_source(cls, row: Any) -> PaymentSourceDTO | None:
        if not row.source_type and not row.source_payment_id:
            return None

        return PaymentSourceDTO(
            type=row.source_type,
            payment_id=row.source_payment_id,
            payment_method=row.payment_method,
        )

    @classmethod
    def _map_applied_coupon(cls, row: Any) -> AppliedCouponDTO | None:
        if row.applied_coupon_id is None:
            return None

        return AppliedCouponDTO(
            coupon_id=row.applied_coupon_id,
            discount=MoneyDTO(
                amount=row.discount_amount,
                currency=row.discount_currency,
            ),
        )

    @classmethod
    def _map_coupon(cls, row: Any) -> CouponDTO | None:
        if row.applied_coupon_id is None:
            return None

        return CouponDTO(
            id=row.coupon_id,
            creator_id=row.coupon_creator_id,
            code=row.coupon_code,
            discount=DiscountMapper.to_dto(src=row.coupon_discount),
            valid_from=row.coupon_valid_from,
            valid_until=row.coupon_valid_until,
            created_at=row.coupon_created_at,
            is_revoked=row.coupon_is_revoked,
        )
