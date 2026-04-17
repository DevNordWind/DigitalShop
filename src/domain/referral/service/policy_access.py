from domain.user.enums import UserRole


class ReferralPolicyAccessService:
    @classmethod
    def can_update_percent(cls, updater_role: UserRole) -> bool:
        return updater_role >= UserRole.ADMIN
