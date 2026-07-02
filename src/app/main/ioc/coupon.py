from dishka import Provider, Scope, provide, provide_all

from app.app.coupon.cmd import CreateCoupon, RevokeCoupon
from app.app.coupon.port import CouponReader
from app.app.coupon.query import GetCoupon, ListCoupons
from app.domain.coupon.port import CouponRedemptionRepository, CouponRepository
from app.domain.coupon.service import CouponDomainService, CouponRedemptionDomainService
from app.infra.coupon import (
    SqlACouponReader,
    SqlACouponRedemptionRepository,
    SqlACouponRepository,
)


class CouponDomainServicesProvider(Provider):
    scope = Scope.APP

    services = provide_all(CouponDomainService, CouponRedemptionDomainService)


class CouponHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(CreateCoupon, RevokeCoupon)

    queries = provide_all(GetCoupon, ListCoupons)


class CouponAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        provide(SqlACouponRepository, provides=CouponRepository),
        provide(SqlACouponRedemptionRepository, provides=CouponRedemptionRepository),
    )

    reader = provide(SqlACouponReader, provides=CouponReader)
