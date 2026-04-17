from dishka import Provider, Scope, provide

from app.report.port import Reporter
from infra.report.reporter import ReporterImpl


class ReportAdaptersProvider(Provider):
    scope = Scope.REQUEST

    reporter = provide(ReporterImpl, provides=Reporter)
