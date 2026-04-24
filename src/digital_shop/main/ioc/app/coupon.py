from app.coupon.cmd import CreateCoupon, RevokeCoupon
from app.coupon.query import GetCoupon, ListCoupons
from dishka import Provider, Scope, provide_all


class CouponHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(CreateCoupon, RevokeCoupon)

    queries = provide_all(GetCoupon, ListCoupons)
