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
        provide(CategoryService),
        provide(CategoryMediaKeyFactory),
    )

    payment_service = provide_all(
        provide(PaymentService),
        provide(PaymentCommissionRuleFactory),
    )

    position_services = provide_all(
        provide(PositionService),
        provide(PositionMediaKeyFactory),
        provide(ItemFactory),
        provide(ItemContentFactory),
    )

    position_warehouse_service = provide(
        PositionWarehouseService,
        scope=Scope.REQUEST,
    )

    coupon_services = provide_all(
        provide(CouponService),
        provide(CouponRedemptionService),
    )

    referral_services = provide_all(
        provide(ReferralAwardService),
        provide(ReferrerProfileService),
    )

    order_service = provide(OrderService)
