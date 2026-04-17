from dishka import Provider, Scope, provide, provide_all

from app.order.cmd import (
    ApplyCouponToOrder,
    CancelOrder,
    ChangeOrderCurrency,
    ChangeOrderItemsAmount,
    ConfirmOrder,
    ConfirmOrderWithDiscount,
    CreateOrder,
    ExpireOutdatedOrders,
    PayOrderWithPayment,
    PayOrderWithWallet,
)
from app.order.query import GetOrder, ListOrders


class OrderHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        provide(ApplyCouponToOrder),
        provide(CancelOrder),
        provide(ChangeOrderCurrency),
        provide(ChangeOrderItemsAmount),
        provide(
            ConfirmOrder,
        ),
        provide(CreateOrder),
        provide(PayOrderWithWallet),
        provide(PayOrderWithPayment),
        provide(ConfirmOrderWithDiscount),
        provide(ExpireOutdatedOrders),
    )

    queries = provide_all(GetOrder, ListOrders)
