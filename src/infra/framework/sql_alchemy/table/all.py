from .category import map_category
from .coupon import map_coupon, map_coupon_redemption
from .order import map_order
from .payment import map_payment, map_payment_commission_rule
from .position import map_item, map_position
from .referral import (
    map_referral_award,
    map_referral_policy,
    map_referrer_profile,
)
from .telegram_context import map_telegram_context
from .user import map_user
from .wallet import map_wallet


def map_all() -> None:
    map_user()
    map_telegram_context()
    map_category()
    map_payment()
    map_payment_commission_rule()
    map_wallet()
    map_position()
    map_item()
    map_coupon()
    map_coupon_redemption()
    map_order()
    map_referral_policy()
    map_referrer_profile()
    map_referral_award()
