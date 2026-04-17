from domain.common.money import Currency, Money
from domain.common.port import Clock, UUIDProvider
from domain.order.entity import Order
from domain.order.enums import OrderStatus
from domain.order.value_object import OrderId, PositionSnapshot
from domain.product.position.entity import Position
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.product.position.value_object import PositionPrice
from domain.user.entity import User


class OrderService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        customer: User,
        position: Position,
        items_amount: ItemsAmount,
        customer_currency: Currency,
    ) -> Order:
        sub_total = self._calculate_sub_total(
            position.price,
            items_amount,
            customer_currency,
        )

        snapshot = PositionSnapshot(
            category_id=position.category_id.value,
            position_id=position.id.value,
            price=position.price,
            position_name=position.name,
        )

        return Order(
            id=OrderId(self._uuid()),
            customer_id=customer.id,
            status=OrderStatus.NEW,
            position=snapshot,
            items=None,
            items_amount=items_amount,
            sub_total=sub_total,
            created_at=self._clock.now(),
        )

    def change_currency(
        self,
        order: Order,
        new_customer_currency: Currency,
    ) -> None:
        sub_total = self._calculate_sub_total(
            price=order.position.price,
            items_amount=order.items_amount,
            customer_currency=new_customer_currency,
        )
        order.change_currency(recalculated_sub_total=sub_total)

    def change_items_amount(
        self,
        order: Order,
        new_items_amount: ItemsAmount,
    ) -> None:
        sub_total = self._calculate_sub_total(
            price=order.position.price,
            items_amount=new_items_amount,
            customer_currency=order.sub_total.currency,
        )
        order.change_items_amount(
            recalculated_sub_total=sub_total,
            new_items_amount=new_items_amount,
        )

    def _calculate_sub_total(
        self,
        price: PositionPrice,
        items_amount: ItemsAmount,
        customer_currency: Currency,
    ) -> Money:
        cost: Money = price.get(customer_currency)

        return Money(
            amount=cost.amount * items_amount.value,
            currency=cost.currency,
        )
