from app.user.cmd import AssignUserRole, RegisterUser
from app.user.query import GetUserProfileReport
from app.user.service import GetCurrentUser
from dishka import Provider, Scope, provide_all


class UserHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(RegisterUser, AssignUserRole)

    queries = provide_all(GetUserProfileReport)

    service = GetCurrentUser
