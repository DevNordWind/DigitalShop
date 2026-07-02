from .common import CommonAdaptersProvider
from .config import ConfigurationProvider
from .coupon import (
    CouponAdaptersProvider,
    CouponDomainServicesProvider,
    CouponHandlersProvider,
)
from .framework import (
    AiogramProvider,
    CryptoBotProvider,
    GoogleTranslatorProvider,
    RedisProvider,
    RetortProvider,
    SqlAlchemyProvider,
    TaskIqActorProvider,
    TaskIqProvider,
)
from .order import (
    OrderAdaptersProvider,
    OrderDomainServicesProvider,
    OrderHandlersProvider,
)
from .payment import (
    PaymentAdaptersProvider,
    PaymentDomainServicesProvider,
    PaymentHandlersProvider,
)
from .providers import PROVIDERS
from .referral import (
    ReferralAdaptersProvider,
    ReferralDomainServicesProvider,
    ReferralHandlersProvider,
)
from .report import ReportAdaptersProvider, ReportHandlersProvider
from .shopping import (
    ShoppingAdaptersProvider,
    ShoppingDomainServicesProvider,
    ShoppingHandlersProvider,
)
from .user import UserAdaptersProvider, UserDomainServicesProvider, UserHandlersProvider
from .wallet import WalletAdaptersProvider, WalletHandlersProvider

__all__ = (
    "PROVIDERS",
    "AiogramProvider",
    "CommonAdaptersProvider",
    "ConfigurationProvider",
    "CouponAdaptersProvider",
    "CouponDomainServicesProvider",
    "CouponHandlersProvider",
    "CryptoBotProvider",
    "GoogleTranslatorProvider",
    "OrderAdaptersProvider",
    "OrderDomainServicesProvider",
    "OrderHandlersProvider",
    "PaymentAdaptersProvider",
    "PaymentDomainServicesProvider",
    "PaymentHandlersProvider",
    "RedisProvider",
    "ReferralAdaptersProvider",
    "ReferralDomainServicesProvider",
    "ReferralHandlersProvider",
    "ReportAdaptersProvider",
    "ReportHandlersProvider",
    "RetortProvider",
    "ShoppingAdaptersProvider",
    "ShoppingDomainServicesProvider",
    "ShoppingHandlersProvider",
    "SqlAlchemyProvider",
    "TaskIqActorProvider",
    "TaskIqProvider",
    "UserAdaptersProvider",
    "UserDomainServicesProvider",
    "UserHandlersProvider",
    "WalletAdaptersProvider",
    "WalletHandlersProvider",
)
