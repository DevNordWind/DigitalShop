from app.domain.common.actor import Actor, SystemActor, UserActor
from app.domain.order.enums import OrderAccessLevel, OrderStatus
from app.domain.order.exception import OrderPermissionDeniedError
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


class OrderAccessService:
    @classmethod
    def ensure_can_create(cls, actor: Actor) -> UserActor:
        if isinstance(actor, SystemActor):
            raise OrderPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_change_currency(cls, actor: Actor, customer_id: UserId) -> UserActor:
        if isinstance(actor, SystemActor):
            raise OrderPermissionDeniedError

        if actor.id != customer_id:
            raise OrderPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_apply_coupon(cls, actor: Actor, customer_id: UserId) -> UserActor:
        if isinstance(actor, SystemActor):
            raise OrderPermissionDeniedError

        if actor.id != customer_id:
            raise OrderPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_checkout(cls, actor: Actor, customer_id: UserId) -> UserActor:
        if isinstance(actor, SystemActor):
            raise OrderPermissionDeniedError

        if actor.id != customer_id:
            raise OrderPermissionDeniedError

        return actor

    @classmethod
    def ensure_can_view(cls, actor: Actor, customer_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == customer_id:
            return

        raise OrderPermissionDeniedError

    @classmethod
    def determine_access_level(
        cls,
        actor: Actor,
        customer_id: UserId,
        order_status: OrderStatus,
    ) -> OrderAccessLevel:
        if isinstance(actor, SystemActor):
            return OrderAccessLevel.FULL

        if actor.role >= UserRole.ADMIN:
            return OrderAccessLevel.FULL

        if actor.id != customer_id:
            raise OrderPermissionDeniedError

        if order_status == OrderStatus.CONFIRMED:
            return OrderAccessLevel.FULL

        return OrderAccessLevel.PREVIEW

    @classmethod
    def ensure_can_cancel(cls, actor: Actor, customer_id: UserId) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        if actor.id == customer_id:
            return

        raise OrderPermissionDeniedError
