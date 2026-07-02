from app.domain.common.actor import Actor, SystemActor
from app.domain.referral.exception import ReferralPolicyPermissionDeniedError
from app.domain.user.enums import UserRole


class ReferralPolicyAccessService:
    @classmethod
    def ensure_can_update_percent(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise ReferralPolicyPermissionDeniedError
