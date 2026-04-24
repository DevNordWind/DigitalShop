from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.value_object import UserId


class PaymentAccessService:
    @classmethod
    def can_view(cls, viewer: User, payment_creator_id: UserId) -> bool:
        if viewer.role >= UserRole.ADMIN:
            return True

        return viewer.id == payment_creator_id
