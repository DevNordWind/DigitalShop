from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.referral.exception import ReferrerProfilePermissionDeniedError
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


class ReferrerProfileAccessService:
    @classmethod
    def ensure_can_create(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise ReferrerProfilePermissionDeniedError

        return actor

    @classmethod
    def ensure_can_view(cls, actor: Actor, profile_user_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == profile_user_id:
            return

        raise ReferrerProfilePermissionDeniedError

    @classmethod
    def ensure_can_change(cls, actor: Actor, profile_user_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == profile_user_id:
            return

        raise ReferrerProfilePermissionDeniedError
