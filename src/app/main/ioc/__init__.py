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
    DishkaTaskIqActorProvider,
    GoogleTranslatorProvider,
    RedisProvider,
    RetortProvider,
    SqlAlchemyProvider,
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
from .presentation import (
    AiogramAdaptersProvider,
    DishkaFastAPIActorProvider,
    TelegramAdaptersProvider,
    TelegramAuthenticationHandlersProvider,
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
    "AiogramAdaptersProvider",
    "AiogramProvider",
    "CommonAdaptersProvider",
    "ConfigurationProvider",
    "CouponAdaptersProvider",
    "CouponDomainServicesProvider",
    "CouponHandlersProvider",
    "CryptoBotProvider",
    "DishkaFastAPIActorProvider",
    "DishkaTaskIqActorProvider",
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
    "TaskIqProvider",
    "TelegramAdaptersProvider",
    "TelegramAuthenticationHandlersProvider",
    "UserAdaptersProvider",
    "UserDomainServicesProvider",
    "UserHandlersProvider",
    "WalletAdaptersProvider",
    "WalletHandlersProvider",
)
