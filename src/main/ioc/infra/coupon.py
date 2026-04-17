from dishka import Provider, Scope, provide

from app.coupon.port import CouponReader
from domain.coupon.port import CouponRedemptionRepository, CouponRepository
from infra.coupon.reader import CouponReaderImpl
from infra.coupon.redemption_repository import CouponRedemptionRepositoryImpl
from infra.coupon.repository import CouponRepositoryImpl


class CouponAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(CouponRepositoryImpl, provides=CouponRepository)

    reader = provide(CouponReaderImpl, provides=CouponReader)

    redemption_repository = provide(
        CouponRedemptionRepositoryImpl,
        provides=CouponRedemptionRepository,
    )
