from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.coupon.entity import Coupon
from app.domain.coupon.exception import CouponNotFoundError
from app.domain.coupon.port import CouponRepository
from app.domain.coupon.service import CouponAccessService
from app.domain.coupon.value_object import CouponId


@dataclass(slots=True, frozen=True)
class RevokeCouponCmd:
    id: UUID


class RevokeCoupon:
    def __init__(
        self,
        repository: CouponRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repository = repository
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: RevokeCouponCmd) -> None:
        CouponAccessService.ensure_can_revoke(actor=await self._actor_provider.get())

        coupon: Coupon | None = await self._repository.get(coupon_id=CouponId(cmd.id))
        if not coupon:
            raise CouponNotFoundError

        coupon.revoke()
        await self._session.commit()
