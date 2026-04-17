from domain.product.position.enums import PositionStatus
from domain.product.position.exception import PositionPermissionDenied
from domain.user.enums import UserRole


class PositionAccessService:
    @classmethod
    def can_create(cls, creator_role: UserRole) -> bool:
        return creator_role >= UserRole.ADMIN

    @classmethod
    def can_edit(cls, editor_role: UserRole) -> bool:
        return editor_role >= UserRole.ADMIN

    @classmethod
    def can_add_item(cls, creator_role: UserRole) -> bool:
        return creator_role >= UserRole.ADMIN

    @classmethod
    def can_replace_item(cls, replacer_role: UserRole) -> bool:
        return replacer_role >= UserRole.ADMIN

    @classmethod
    def can_delete_item(cls, deleter_role: UserRole) -> bool:
        return deleter_role >= UserRole.ADMIN

    @classmethod
    def can_delete(cls, deleter_role: UserRole) -> bool:
        return deleter_role >= UserRole.ADMIN

    @classmethod
    def can_archive(cls, archiver_role: UserRole) -> bool:
        return archiver_role >= UserRole.ADMIN

    @classmethod
    def can_archive_item(cls, archiver_role: UserRole) -> bool:
        return archiver_role >= UserRole.ADMIN

    @classmethod
    def can_view_archived(cls, viewer_role: UserRole) -> bool:
        return viewer_role >= UserRole.ADMIN

    @classmethod
    def can_view_item(cls, viewer_role: UserRole) -> bool:
        return viewer_role >= UserRole.ADMIN

    @classmethod
    def can_recover(cls, recoverer_role: UserRole) -> bool:
        return recoverer_role >= UserRole.ADMIN

    @classmethod
    def resolve_visible_status(
        cls,
        viewer_role: UserRole,
        requested_status: PositionStatus | None,
    ) -> PositionStatus | None:
        if cls.can_view_archived(viewer_role):
            return requested_status

        if requested_status == PositionStatus.ARCHIVED:
            raise PositionPermissionDenied

        return requested_status or PositionStatus.AVAILABLE
