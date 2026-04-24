from dataclasses import dataclass

from app.payment.dto.commission import CommissionMapper
from app.payment.dto.commission.dto import CommissionDTO
from domain.payment.enums import PaymentMethod
from domain.payment.port import PaymentCommissionRuleRepository
from domain.payment.rule import PaymentCommissionRule


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
