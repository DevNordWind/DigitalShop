from dishka import Provider, Scope, provide

from app.product.position.port import PositionReader
from domain.product.position.port import PositionRepository
from infra.position.reader import PositionReaderImpl
from infra.position.repository import PositionRepositoryImpl


class PositionAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(PositionRepositoryImpl, provides=PositionRepository)

    reader = provide(PositionReaderImpl, provides=PositionReader)
