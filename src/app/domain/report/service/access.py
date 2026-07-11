from app.domain.common.actor import Actor, SystemActor
from app.domain.report.exception import ReportPermissionDeniedError
from app.domain.user.enums import UserRole


class ReportAccessService:
    @classmethod
    def ensure_can_get_general(cls, actor: Actor) -> None:
        if isinstance(actor, SystemActor):
            return

        if actor.role >= UserRole.ADMIN:
            return

        raise ReportPermissionDeniedError
