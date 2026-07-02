from dataclasses import dataclass

from app.app.common.dto.coefficient import CoefficientDTO, CoefficientMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.referral.policy import ReferralPolicy
from app.domain.referral.port import ReferralPolicyRepository
from app.domain.referral.service import ReferralPolicyAccessService


@dataclass(slots=True, frozen=True)
class SetReferralCoefficientCmd:
    coefficient: CoefficientDTO


class SetReferralCoefficient:
    def __init__(
        self,
        repo: ReferralPolicyRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repo: ReferralPolicyRepository = repo
        self._session: DatabaseSession = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: SetReferralCoefficientCmd) -> None:
        ReferralPolicyAccessService.ensure_can_update_percent(
            actor=await self._actor_provider.get()
        )

        coefficient = CoefficientMapper.to_value_object(src=cmd.coefficient)

        policy: ReferralPolicy = await self._repo.get()
        policy.change_coefficient(new_coefficient=coefficient)

        await self._session.commit()
