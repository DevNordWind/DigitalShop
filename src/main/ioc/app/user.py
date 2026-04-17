from dishka import Provider, Scope, provide, provide_all

from app.user.cmd import AssignUserRole, RegisterUser
from app.user.query import GetUserProfileReport
from app.user.service import GetCurrentUser


class UserHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(provide(RegisterUser), provide(AssignUserRole))

    queries = provide_all(provide(GetUserProfileReport))

    service = provide(GetCurrentUser)
