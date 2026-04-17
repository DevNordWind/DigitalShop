from domain.product.category.enums import CategoryStatus
from domain.product.category.exception import CategoryAccessDenied
from domain.user.entity import User
from domain.user.enums import UserRole


class CategoryAccessService:
    @classmethod
    def can_create(cls, creator: User) -> bool:
        return creator.role >= UserRole.ADMIN

    @classmethod
    def can_edit(cls, editor: User) -> bool:
        return editor.role >= UserRole.ADMIN

    @classmethod
    def can_archive(cls, archiver: User) -> bool:
        return archiver.role >= UserRole.ADMIN

    @classmethod
    def can_recover(cls, recoverer: User) -> bool:
        return recoverer.role >= UserRole.ADMIN

    @classmethod
    def can_view_archived(cls, viewer_role: UserRole) -> bool:
        return viewer_role >= UserRole.ADMIN

    @classmethod
    def can_delete(cls, deleter: User) -> bool:
        return deleter.role >= UserRole.ADMIN

    @classmethod
    def resolve_visible_status(
        cls,
        viewer_role: UserRole,
        requested_status: CategoryStatus | None,
    ) -> CategoryStatus | None:
        if cls.can_view_archived(viewer_role):
            return requested_status

        if requested_status == CategoryStatus.ARCHIVED:
            raise CategoryAccessDenied

        return requested_status or CategoryStatus.AVAILABLE
