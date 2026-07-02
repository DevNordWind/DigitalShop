from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.exception import CategoryPermissionDeniedError
from app.domain.user.enums import UserRole


class CategoryAccessService:
    @classmethod
    def ensure_can_create(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise CategoryPermissionDeniedError

        if actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_edit(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

    @classmethod
    def ensure_can_archive(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

    @classmethod
    def ensure_can_recover(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

    @classmethod
    def ensure_can_delete(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

    @classmethod
    def ensure_can_view(cls, actor: Actor, category_status: CategoryStatus) -> None:
        if isinstance(actor, SystemActor):
            return

        if category_status == CategoryStatus.ARCHIVED and actor.role < UserRole.ADMIN:
            raise CategoryPermissionDeniedError

    @classmethod
    def resolve_visible_status(
        cls,
        actor: Actor,
        requested_status: CategoryStatus | None,
    ) -> CategoryStatus | None:
        if isinstance(actor, SystemActor) or actor.role >= UserRole.ADMIN:
            return requested_status

        if requested_status == CategoryStatus.ARCHIVED:
            raise CategoryPermissionDeniedError

        if requested_status is None:
            return CategoryStatus.AVAILABLE

        return requested_status
