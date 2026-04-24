from dataclasses import dataclass
from datetime import datetime
from typing import Final

from app.coupon.dto.discount import DiscountDTO
from domain.common.money import Currency

CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True, kw_only=True)
class CouponCreationCtx:
    valid_from: datetime | None = None
    valid_until: datetime | None = None

    code: str | None = None

    discount: DiscountDTO | None = None
    current_currency: Currency

    @property
    def can_create(self) -> bool:
        return self.code is not None and self.discount is not None
