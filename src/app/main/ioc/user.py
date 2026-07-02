from dishka import Provider, Scope, provide, provide_all

from app.app.user.cmd import AssignUserRole
from app.app.user.port import UserReader
from app.app.user.query import GetUserProfile
from app.app.user.service import UserApplicationService
from app.domain.user.port import UserRepository
from app.domain.user.service import UserDomainService
from app.infra.user import SqlAUserReader, SqlAUserRepository


class UserDomainServicesProvider(Provider):
    scope = Scope.APP

    service = provide(UserDomainService)


class UserHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(AssignUserRole)

    services = provide_all(UserApplicationService)

    queries = provide_all(GetUserProfile)


class UserAdaptersProvider(Provider):
    scope = Scope.REQUEST

    reader = provide(SqlAUserReader, provides=UserReader)

    repository = provide(SqlAUserRepository, provides=UserRepository)
