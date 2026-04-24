from dishka import Provider, Scope, provide, provide_all
from domain.coupon.service import CouponRedemptionService
from domain.coupon.service.service import CouponService
from domain.order.service import OrderService
from domain.payment.factory import PaymentCommissionRuleFactory
from domain.payment.service import PaymentService
from domain.product.category.service import (
    CategoryMediaKeyFactory,
    CategoryService,
)
from domain.product.position.item.factory import (
    ItemContentFactory,
    ItemFactory,
)
from domain.product.position.service import (
    PositionMediaKeyFactory,
    PositionService,
    PositionWarehouseService,
)
from domain.referral.service import (
    ReferralAwardService,
    ReferrerProfileService,
)
from domain.user.service import UserService


class DomainServicesProvider(Provider):
    scope = Scope.APP

    user_service = provide(UserService)

    category_services = provide_all(
        CategoryService,
        CategoryMediaKeyFactory,
    )

    payment_service = provide_all(
        PaymentService,
        PaymentCommissionRuleFactory,
    )

    position_services = provide_all(
        PositionService,
        PositionMediaKeyFactory,
        ItemFactory,
        ItemContentFactory,
    )

    position_warehouse_service = provide(
        PositionWarehouseService,
        scope=Scope.REQUEST,
    )

    coupon_services = provide_all(
        CouponService,
        CouponRedemptionService,
    )

    referral_services = provide_all(
        ReferralAwardService,
        ReferrerProfileService,
    )

    order_service = provide(OrderService)
