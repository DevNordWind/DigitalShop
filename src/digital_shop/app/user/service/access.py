from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.value_object import UserId


class UserReporterAccessService:
    @classmethod
    def can_get_profile_report(
        cls,
        requestor: User,
        target_user_id: UserId,
    ) -> bool:
        if requestor.role >= UserRole.ADMIN:
            return True

        return requestor.id == target_user_id
