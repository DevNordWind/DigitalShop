from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.value_object import UserId


class WalletAccessService:
    @classmethod
    def can_top_up_payment(
        cls,
        actor_user_id: UserId,
        actor_role: UserRole,
        wallet_user_id: UserId,
    ) -> bool:
        if actor_role >= UserRole.ADMIN:
            return True
        return wallet_user_id == actor_user_id

    @classmethod
    def can_top_up_manually(
        cls,
        actor_role: UserRole,
    ) -> bool:
        return actor_role >= UserRole.ADMIN

    @classmethod
    def can_view(cls, viewer: User, wallet_user_id: UserId) -> bool:
        if viewer.role >= UserRole.ADMIN:
            return True

        return wallet_user_id == viewer.id
