from dataclasses import dataclass

from app.app.payment.dto.commission import CommissionDTO, CommissionMapper
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.port import PaymentCommissionRuleRepository
from app.domain.payment.rule import PaymentCommissionRule


@dataclass(slots=True, frozen=True)
class GetPaymentCommissionQuery:
    method: PaymentMethod


class GetPaymentCommission:
    def __init__(self, repo: PaymentCommissionRuleRepository):
        self._repo: PaymentCommissionRuleRepository = repo

    async def __call__(
        self,
        query: GetPaymentCommissionQuery,
    ) -> CommissionDTO:
        rule: PaymentCommissionRule = await self._repo.get(method=query.method)

        return CommissionMapper.to_dto(src=rule)
