from app.report.query import GetConvertedGeneralReport
from dishka import Provider, Scope, provide_all


class ReportHandlersProvider(Provider):
    scope = Scope.REQUEST

    queries = provide_all(GetConvertedGeneralReport)
