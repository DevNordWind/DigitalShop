from domain.user.enums import UserRole


class PositionSettingsAccessService:
    @classmethod
    def can_edit(cls, editor_role: UserRole) -> bool:
        return editor_role >= UserRole.ADMIN
