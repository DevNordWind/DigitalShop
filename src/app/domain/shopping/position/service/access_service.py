from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.exception import PositionPermissionDeniedError
from app.domain.user.enums import UserRole


class PositionAccessService:
    @classmethod
    def ensure_can_create(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise PositionPermissionDeniedError

        if actor.role >= UserRole.ADMIN:
            return actor

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_edit(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_add_item(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise PositionPermissionDeniedError

        if actor.role >= UserRole.ADMIN:
            return actor

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_replace_item(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_delete_item(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_delete(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_archive(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_archive_item(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_view(cls, actor: Actor, position_status: PositionStatus) -> None:
        if isinstance(actor, SystemActor):
            return

        if position_status == PositionStatus.ARCHIVED and actor.role < UserRole.ADMIN:
            raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_view_item(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def ensure_can_recover(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise PositionPermissionDeniedError

    @classmethod
    def resolve_visible_status(
        cls,
        actor: Actor,
        requested_status: PositionStatus | None,
    ) -> PositionStatus | None:
        if isinstance(actor, SystemActor):
            return requested_status
        if actor.role >= UserRole.ADMIN:
            return requested_status

        if requested_status == PositionStatus.ARCHIVED:
            raise PositionPermissionDeniedError

        return requested_status or PositionStatus.AVAILABLE
