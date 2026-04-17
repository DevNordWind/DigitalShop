from domain.user.enums import UserRole


class ReporterAccessService:
    @classmethod
    def can_get_general(cls, role: UserRole) -> bool:
        return role >= UserRole.ADMIN
