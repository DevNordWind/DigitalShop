from frozendict import frozendict

from app.domain.common.exception import DomainError
from app.domain.common.localized import Language
from app.domain.coupon.exception import (
    CouponAlreadyExistsError,
    CouponAlreadyUsedByUserError,
)
from app.domain.payment.exception import PaymentCommissionRuleAlreadyExistsError
from app.domain.referral.exception import ReferrerProfileAlreadyExistsError
from app.domain.shopping.category.exception import CategoryNameAlreadyTakenError
from app.domain.shopping.position.exception import PositionNameAlreadyTakenError


class IntegrityErrorMapper:
    MAPPING: frozendict[str, DomainError] = frozendict(
        {
            f"uq_category_name_values_{lang.value}": CategoryNameAlreadyTakenError(
                lang=lang,
            )
            for lang in Language
        }
        | {
            f"uq_Position_name_values_{lang.value}": PositionNameAlreadyTakenError(
                lang=lang,
            )
            for lang in Language
        }
        | {
            "uq_Coupon_code": CouponAlreadyExistsError(),
            "pk_ReferrerProfile": ReferrerProfileAlreadyExistsError(),
            "uq_coupon_user_not_cancelled": CouponAlreadyUsedByUserError(),
            "pk_PaymentCommissionRule": PaymentCommissionRuleAlreadyExistsError(),
        },
    )

    @classmethod
    def to_domain(cls, constraint: str) -> DomainError | None:
        return cls.MAPPING.get(constraint)
