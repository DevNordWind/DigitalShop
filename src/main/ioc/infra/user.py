from dishka import Provider, Scope, provide

from app.user.port.reporter import UserReporter
from domain.user.port import UserRepository
from infra.user.reporter import UserReporterImpl
from infra.user.repository import UserRepositoryImpl


class UserAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(UserRepositoryImpl, provides=UserRepository)

    reporter = provide(UserReporterImpl, provides=UserReporter)
