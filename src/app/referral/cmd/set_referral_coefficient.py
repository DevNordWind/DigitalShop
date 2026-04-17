from dataclasses import dataclass

from app.common.dto.coefficient import CoefficientDTO, CoefficientMapper
from app.common.port import DatabaseSession
from app.user.port import UserIdentifyProvider
from domain.referral.exception import ReferralPolicyPermissionDenied
from domain.referral.policy import ReferralPolicy
from domain.referral.port import ReferralPolicyRepository
from domain.referral.service import ReferralPolicyAccessService


@dataclass(slots=True, frozen=True)
class SetReferralCoefficientCmd:
    coefficient: CoefficientDTO


class SetReferralCoefficient:
    def __init__(
        self,
        repo: ReferralPolicyRepository,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: ReferralPolicyRepository = repo
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: SetReferralCoefficientCmd) -> None:
        if not ReferralPolicyAccessService.can_update_percent(
            updater_role=await self._idp.get_role()
        ):
            raise ReferralPolicyPermissionDenied

        coefficient = CoefficientMapper.to_value_object(src=cmd.coefficient)

        policy: ReferralPolicy = await self._repo.get()
        policy.change_coefficient(new_coefficient=coefficient)

        await self._session.commit()
