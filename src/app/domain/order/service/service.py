from app.domain.common.money import Currency, Money
from app.domain.common.port import Clock, UUIDProvider
from app.domain.order.entity import Order
from app.domain.order.enums import OrderStatus
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.item.value_object import ItemsAmount
from app.domain.shopping.position.value_object import PositionPrice, PositionSnapshot
from app.domain.user.value_object import UserId


class OrderDomainService:
    def __init__(self, uuid_provider: UUIDProvider, clock: Clock):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock

    def create(
        self,
        customer_id: UserId,
        position: Position,
        items_amount: ItemsAmount,
        customer_currency: Currency,
    ) -> Order:
        position_snapshot: PositionSnapshot = position.take_snapshot()

        return Order(
            id=OrderId(self._uuid()),
            customer_id=customer_id,
            status=OrderStatus.NEW,
            position=position_snapshot,
            items=None,
            items_amount=items_amount,
            sub_total=self._calculate_sub_total(
                price=position_snapshot.price,
                customer_currency=customer_currency,
                items_amount=items_amount,
            ),
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
