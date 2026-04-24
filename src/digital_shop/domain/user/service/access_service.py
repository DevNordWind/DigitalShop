from domain.user.enums import UserRole


class UserAccessService:
    @classmethod
    def can_assign_role(
        cls,
        assigner_role: UserRole,
        target_current_role: UserRole,
        target_role: UserRole,
    ) -> bool:
        return assigner_role > max(target_current_role, target_role)
