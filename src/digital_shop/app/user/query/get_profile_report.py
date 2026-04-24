from dataclasses import dataclass
from uuid import UUID

from app.user.dto.report import UserProfileReport
from app.user.exception import UserNotFound, UserReporterPermissionDenied
from app.user.port import UserIdentifyResolver
from app.user.port.reporter import UserReporter
from app.user.service import GetCurrentUser
from app.user.service.access import UserReporterAccessService
from domain.user.entity import User
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetUserProfileReportQuery:
    target_identifier: str | UUID


class GetUserProfileReport:
    def __init__(
        self,
        reporter: UserReporter,
        current_user: GetCurrentUser,
        idr: UserIdentifyResolver,
    ):
        self._reporter: UserReporter = reporter
        self._current_user: GetCurrentUser = current_user
        self._idr: UserIdentifyResolver = idr

    async def __call__(
        self, query: GetUserProfileReportQuery
    ) -> UserProfileReport:
        target_user_id: UserId | None = await self._idr.resolve(
            identifier=query.target_identifier
        )
        if target_user_id is None:
            raise UserNotFound

        requestor: User = await self._current_user()

        if not UserReporterAccessService.can_get_profile_report(
            requestor=requestor, target_user_id=target_user_id
        ):
            raise UserReporterPermissionDenied

        report: UserProfileReport | None = await self._reporter.report_profile(
            target_user_id=target_user_id
        )
        if not report:
            raise UserNotFound

        return report
