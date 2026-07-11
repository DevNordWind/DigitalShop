from app.domain.common.actor import Actor, SystemActor
from app.domain.payment.exception import PaymentPermissionDeniedError
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


class PaymentAccessService:
    @classmethod
    def ensure_can_view(cls, actor: Actor, payment_creator_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == payment_creator_id:
            return

        raise PaymentPermissionDeniedError
