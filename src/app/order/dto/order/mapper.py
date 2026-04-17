from app.order.dto.order.order import OrderDTO, PublicOrderDTO


class OrderMapper:
    @classmethod
    def to_public(cls, src: OrderDTO) -> PublicOrderDTO:
        return PublicOrderDTO(
            id=src.id,
            customer_id=src.customer_id,
            sub_total=src.sub_total,
            total=src.total,
            status=src.status,
            source=src.source,
            created_at=src.created_at,
            confirmed_at=src.confirmed_at,
            cancelled_at=src.cancelled_at,
            applied_coupon=src.applied_coupon,
            position=src.position,
            failed_at=src.failed_at,
            items_amount=src.items_amount,
            coupon=src.coupon,
            awaited_payment_at=src.awaited_payment_at,
        )
