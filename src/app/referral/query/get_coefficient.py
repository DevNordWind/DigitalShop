from app.common.dto.coefficient import CoefficientDTO, CoefficientMapper
from domain.referral.policy import ReferralPolicy
from domain.referral.port import ReferralPolicyRepository


class GetReferralCoefficient:
    def __init__(self, repository: ReferralPolicyRepository):
        self._repo: ReferralPolicyRepository = repository

    async def __call__(self) -> CoefficientDTO:
        policy: ReferralPolicy = await self._repo.get()

        return CoefficientMapper.to_dto(src=policy.coefficient)
