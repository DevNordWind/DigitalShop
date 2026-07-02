from dishka import Provider, Scope, provide, provide_all

from app.app.order.cmd import (
    ApplyCouponToOrder,
    CancelOrder,
    ChangeOrderCurrency,
    ChangeOrderItemsAmount,
    ConfirmOrder,
    ConfirmOrderWithDiscount,
    ExpireOutdatedOrders,
    PayOrderWithPayment,
    PayOrderWithWallet,
)
from app.app.order.port import OrderReader
from app.app.order.query import GetOrder, ListOrders
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderDomainService
from app.infra.order import SqlAOrderReader, SqlAOrderRepository


class OrderDomainServicesProvider(Provider):
    scope = Scope.APP

    service = provide(OrderDomainService)


class OrderHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ApplyCouponToOrder,
        CancelOrder,
        ChangeOrderCurrency,
        ChangeOrderItemsAmount,
        ConfirmOrder,
        ConfirmOrderWithDiscount,
        ExpireOutdatedOrders,
        PayOrderWithPayment,
        PayOrderWithWallet,
    )

    queries = provide_all(GetOrder, ListOrders)


class OrderAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(SqlAOrderRepository, provides=OrderRepository)

    reader = provide(SqlAOrderReader, provides=OrderReader)
