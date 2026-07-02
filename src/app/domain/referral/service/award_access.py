from app.domain.common.actor import Actor, SystemActor
from app.domain.referral.exception import ReferralAwardPermissionDeniedError
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


class ReferralAwardAccessService:
    @classmethod
    def ensure_can_view(
        cls,
        actor: Actor,
        referrer_id: UserId,
    ) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if referrer_id != actor.id:
            raise ReferralAwardPermissionDeniedError
