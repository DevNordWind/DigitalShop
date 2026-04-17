from dishka import Provider, Scope, provide

from app.product.category.port import CategoryReader
from domain.product.category.port import CategoryRepository
from infra.category.reader import CategoryReaderImpl
from infra.category.repository import CategoryRepositoryImpl


class CategoryAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(CategoryRepositoryImpl, provides=CategoryRepository)

    reader = provide(CategoryReaderImpl, provides=CategoryReader)
