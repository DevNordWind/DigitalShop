from domain.order.enums import OrderStatus
from domain.order.exception import OrderPermissionDenied
from domain.user.enums import UserRole
from domain.user.value_object import UserId


class OrderAccessService:
    @classmethod
    def can_view(
        cls,
        viewer_role: UserRole,
        viewer_id: UserId,
        customer_id: UserId,
    ) -> bool:
        if viewer_role >= UserRole.ADMIN:
            return True

        return viewer_id == customer_id

    @classmethod
    def can_checkout(cls, actor_id: UserId, order_customer_id: UserId) -> bool:
        return actor_id == order_customer_id

    @classmethod
    def can_view_items(
        cls,
        viewer_role: UserRole,
        viewer_id: UserId,
        customer_id: UserId,
        order_status: OrderStatus,
    ) -> bool:
        if viewer_role >= UserRole.ADMIN:
            return True

        if viewer_id != customer_id:
            raise OrderPermissionDenied

        return order_status == OrderStatus.CONFIRMED

    @classmethod
    def can_cancel(
        cls, actor_id: UserId, actor_role: UserRole, order_customer_id: UserId
    ) -> bool:
        if actor_role >= UserRole.ADMIN:
            return True

        return actor_id == order_customer_id
