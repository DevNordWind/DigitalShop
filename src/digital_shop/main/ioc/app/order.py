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
from dishka import Provider, Scope, provide_all


class OrderHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ApplyCouponToOrder,
        CancelOrder,
        ChangeOrderCurrency,
        ChangeOrderItemsAmount,
        ConfirmOrder,
        CreateOrder,
        PayOrderWithWallet,
        PayOrderWithPayment,
        ConfirmOrderWithDiscount,
        ExpireOutdatedOrders,
    )

    queries = provide_all(GetOrder, ListOrders)
