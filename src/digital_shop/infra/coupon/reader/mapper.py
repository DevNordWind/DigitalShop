from typing import Any

from app.coupon.dto.coupon import CouponDTO
from app.coupon.dto.discount import DiscountMapper


class CouponReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> CouponDTO:
        return CouponDTO(
            id=row.id,
            creator_id=row.creator_id,
            code=row.code,
            discount=DiscountMapper.to_dto(src=row.discount),
            valid_from=row.valid_from.value,
            valid_until=row.valid_until.value if row.valid_until else None,
            created_at=row.created_at,
            is_revoked=row.is_revoked,
        )
