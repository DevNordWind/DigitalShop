from .category import CategoryHandlersProvider
from .coupon import CouponHandlersProvider
from .order import OrderHandlersProvider
from .payment import PaymentHandlersProvider
from .position import PositionHandlersProvider
from .referral import ReferralHandlersProvider
from .report import ReportHandlersProvider
from .user import UserHandlersProvider
from .wallet import WalletHandlersProvider

__all__ = (
    "CategoryHandlersProvider",
    "CouponHandlersProvider",
    "OrderHandlersProvider",
    "PaymentHandlersProvider",
    "PositionHandlersProvider",
    "ReferralHandlersProvider",
    "ReportHandlersProvider",
    "UserHandlersProvider",
    "WalletHandlersProvider",
)
