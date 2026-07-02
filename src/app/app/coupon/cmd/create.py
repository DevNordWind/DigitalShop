from dataclasses import dataclass
from datetime import datetime

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.coupon.dto.discount import DiscountDTO, DiscountMapper
from app.domain.common.actor import UserActor
from app.domain.coupon.port import CouponRepository
from app.domain.coupon.service import CouponAccessService, CouponDomainService
from app.domain.coupon.value_object import CouponCode, CouponId


@dataclass(slots=True, frozen=True)
class CreateCouponCmd:
    code: str
    discount: DiscountDTO
    valid_from: datetime | None
    valid_until: datetime | None


class CreateCoupon:
    def __init__(
        self,
        repository: CouponRepository,
        session: DatabaseSession,
        service: CouponDomainService,
        actor_provider: ActorProvider,
    ):
        self._repository = repository
        self._session = session
        self._service = service
        self._actor_provider = actor_provider

    async def __call__(self, cmd: CreateCouponCmd) -> CouponId:
        actor: UserActor = CouponAccessService.ensure_can_create(
            actor=await self._actor_provider.get()
        )

        coupon = self._service.create(
            creator_id=actor.id,
            code=CouponCode(cmd.code),
            discount=DiscountMapper.to_strategy(src=cmd.discount),
            valid_from=cmd.valid_from,
            valid_until=cmd.valid_until,
        )
        coupon_id: CouponId = coupon.id
        await self._repository.add(coupon=coupon)

        await self._session.commit()

        return coupon_id
