from app.domain.common.actor import Actor, SystemActor
from app.domain.payment.exception import PaymentCommissionRulePermissionDeniedError
from app.domain.user.enums import UserRole


class PaymentCommissionRuleAccessService:
    @classmethod
    def ensure_can_change(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PaymentCommissionRulePermissionDeniedError
