from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.domain.wallet.exception.wallet import WalletPermissionDeniedError


class WalletAccessService:
    @classmethod
    def ensure_can_top_up_payment(
        cls,
        actor: Actor,
    ) -> UserActor:
        if isinstance(actor, SystemActor):
            raise WalletPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_cancel_top_up_payment(
        cls,
        actor: Actor,
        user_id: UserId,
    ) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == user_id:
            return

        raise WalletPermissionDeniedError

    @classmethod
    def ensure_can_top_up_manually(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role < UserRole.ADMIN:
            raise WalletPermissionDeniedError

    @classmethod
    def ensure_can_view(cls, actor: Actor, target_user_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if target_user_id != actor.id:
            raise WalletPermissionDeniedError
