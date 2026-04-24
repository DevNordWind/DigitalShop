from domain.common.exception import DomainError
from domain.common.localized import Language
from domain.coupon.exception import (
    CouponAlreadyExists,
    CouponAlreadyUsedByUser,
)
from domain.payment.exception import PaymentCommissionRuleAlreadyExists
from domain.product.category.exception import CategoryNameAlreadyTaken
from domain.product.position.exception import PositionNameAlreadyTaken
from domain.referral.exception import ReferrerProfileAlreadyExists
from frozendict import frozendict


class IntegrityErrorMapper:
    MAPPING: frozendict[str, DomainError] = frozendict(
        {  # type: ignore[arg-type]
            f"uq_category_name_values_{lang.value}": CategoryNameAlreadyTaken(
                lang=lang,
            )
            for lang in Language
        }
        | {
            f"uq_Position_name_values_{lang.value}": PositionNameAlreadyTaken(
                lang=lang,
            )
            for lang in Language
        }
        | {
            "uq_Coupon_code": CouponAlreadyExists(),
            "pk_ReferrerProfile": ReferrerProfileAlreadyExists(),
            "uq_coupon_user_not_cancelled": CouponAlreadyUsedByUser(),
            "pk_PaymentCommissionRule": PaymentCommissionRuleAlreadyExists,
        },
    )

    @classmethod
    def to_domain(cls, constraint: str) -> DomainError | None:
        return cls.MAPPING.get(constraint)
