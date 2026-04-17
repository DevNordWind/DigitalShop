from dishka import Provider, Scope, provide, provide_all

from app.report.query import GetConvertedGeneralReport


class ReportHandlersProvider(Provider):
    scope = Scope.REQUEST

    queries = provide_all(provide(GetConvertedGeneralReport))
