from dishka import Provider, Scope, provide, provide_all

from app.app.report.query import GetConvertedGeneralReport
from app.domain.report.port import Reporter
from app.infra.report import SqlAReporter


class ReportHandlersProvider(Provider):
    scope = Scope.REQUEST

    queries = provide_all(GetConvertedGeneralReport)


class ReportAdaptersProvider(Provider):
    scope = Scope.REQUEST

    reporter = provide(SqlAReporter, provides=Reporter)
