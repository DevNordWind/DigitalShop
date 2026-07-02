from dishka import Provider

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
    TelegramAdaptersProvider,
)
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

PROVIDERS: tuple[Provider, ...] = (
    WalletHandlersProvider(),
    WalletAdaptersProvider(),
    UserAdaptersProvider(),
    UserHandlersProvider(),
    UserDomainServicesProvider(),
    ShoppingAdaptersProvider(),
    ShoppingDomainServicesProvider(),
    ShoppingHandlersProvider(),
    ReportAdaptersProvider(),
    ReportHandlersProvider(),
    ReferralDomainServicesProvider(),
    ReferralHandlersProvider(),
    ReferralAdaptersProvider(),
    PaymentHandlersProvider(),
    PaymentDomainServicesProvider(),
    PaymentAdaptersProvider(),
    OrderAdaptersProvider(),
    OrderHandlersProvider(),
    OrderDomainServicesProvider(),
    CryptoBotProvider(),
    AiogramProvider(),
    GoogleTranslatorProvider(),
    RedisProvider(),
    RetortProvider(),
    SqlAlchemyProvider(),
    TaskIqProvider(),
    CouponAdaptersProvider(),
    CouponDomainServicesProvider(),
    CouponHandlersProvider(),
    ConfigurationProvider(),
    CommonAdaptersProvider(),
    TelegramAdaptersProvider(),
)
