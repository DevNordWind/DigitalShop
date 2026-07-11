from app.domain.common.actor import Actor, SystemActor
from app.domain.user.enums import UserRole
from app.domain.user.exception.user import UserPermissionDeniedError
from app.domain.user.value_object import UserId


class UserAccessService:
    @classmethod
    def ensure_can_view_profile(
        cls,
        actor: Actor,
        target_user_id: UserId,
    ) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == target_user_id:
            return

        raise UserPermissionDeniedError

    @classmethod
    def ensure_can_assign_role(
        cls,
        actor: Actor,
        target_current_role: UserRole,
        target_role: UserRole,
    ) -> None:
        if isinstance(actor, SystemActor):
            return

        if not actor.role > max(target_current_role, target_role):
            raise UserPermissionDeniedError
