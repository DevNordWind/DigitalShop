from domain.user.enums import UserRole
from domain.user.value_object import UserId


class ReferralAwardAccessService:
    @classmethod
    def can_view(
        cls,
        referrer_id: UserId,
        viewer_id: UserId,
        viewer_role: UserRole,
    ) -> bool:
        if viewer_role >= UserRole.ADMIN:
            return True

        return referrer_id == viewer_id
