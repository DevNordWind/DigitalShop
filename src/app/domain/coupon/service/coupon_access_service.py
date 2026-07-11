from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.coupon.exception import CouponPermissionDeniedError
from app.domain.user.enums import UserRole


class CouponAccessService:
    @classmethod
    def ensure_can_create(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise CouponPermissionDeniedError

        if actor.role < UserRole.ADMIN:
            raise CouponPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_revoke(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise CouponPermissionDeniedError

    @classmethod
    def ensure_can_delete(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise CouponPermissionDeniedError

    @classmethod
    def ensure_can_view(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise CouponPermissionDeniedError
