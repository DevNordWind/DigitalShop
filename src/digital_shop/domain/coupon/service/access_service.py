from domain.user.enums import UserRole


class CouponAccessService:
    @classmethod
    def can_create(cls, creator_role: UserRole) -> bool:
        return creator_role >= UserRole.ADMIN

    @classmethod
    def can_revoke(cls, revoker_role: UserRole) -> bool:
        return revoker_role >= UserRole.ADMIN

    @classmethod
    def can_delete(cls, deleter_role: UserRole) -> bool:
        return deleter_role >= UserRole.ADMIN

    @classmethod
    def can_view(cls, viewer_role: UserRole) -> bool:
        return viewer_role >= UserRole.ADMIN
