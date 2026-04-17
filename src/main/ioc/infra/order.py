from dishka import Provider, Scope, provide

from app.order.port.reader import OrderReader
from domain.order.port.repository import OrderRepository
from infra.order import OrderRepositoryImpl
from infra.order.reader import OrderReaderImpl


class OrderAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(OrderRepositoryImpl, provides=OrderRepository)

    reader = provide(OrderReaderImpl, provides=OrderReader)
