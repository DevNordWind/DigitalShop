from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.coupon.exception import CouponNotFound
from app.user.service import GetCurrentUser
from domain.coupon.exception import CouponPermissionDenied
from domain.coupon.port import CouponRepository
from domain.coupon.service.access_service import CouponAccessService
from domain.coupon.value_object import CouponId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class RevokeCouponCmd:
    id: UUID


class RevokeCoupon:
    def __init__(
        self,
        repository: CouponRepository,
        session: DatabaseSession,
        current_user: GetCurrentUser,
    ):
        self._repository: CouponRepository = repository
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user

    async def __call__(self, cmd: RevokeCouponCmd) -> None:
        revoker: User = await self._current_user()

        if not CouponAccessService.can_revoke(revoker_role=revoker.role):
            raise CouponPermissionDenied

        coupon = await self._repository.get(coupon_id=CouponId(cmd.id))
        if not coupon:
            raise CouponNotFound

        coupon.revoke()

        await self._session.commit()
