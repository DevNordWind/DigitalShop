from dishka import Provider, Scope, provide, provide_all

from app.coupon.cmd import CreateCoupon, RevokeCoupon
from app.coupon.query import GetCoupon, ListCoupons


class CouponHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(provide(CreateCoupon), provide(RevokeCoupon))

    queries = provide_all(provide(GetCoupon), provide(ListCoupons))
