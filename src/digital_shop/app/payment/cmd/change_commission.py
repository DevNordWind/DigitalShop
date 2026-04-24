from dataclasses import dataclass

from app.common.dto.coefficient import CoefficientMapper
from app.common.port import DatabaseSession
from app.payment.dto.commission import CommissionDTO
from domain.common.coefficient import Coefficient
from domain.payment.enums import PaymentMethod
from domain.payment.factory import PaymentCommissionRuleFactory
from domain.payment.port import PaymentCommissionRuleRepository
from domain.payment.rule import PaymentCommissionRule


@dataclass(slots=True, frozen=True)
class ChangePaymentCommissionCoefficientCmd:
    method: PaymentMethod
    new_commission: CommissionDTO


class ChangePaymentCommissionCoefficient:
    def __init__(
        self,
        repo: PaymentCommissionRuleRepository,
        session: DatabaseSession,
    ):
        self._repo: PaymentCommissionRuleRepository = repo
        self._session: DatabaseSession = session

    async def __call__(
        self,
        cmd: ChangePaymentCommissionCoefficientCmd,
    ) -> None:
        coefficient: Coefficient | None = None

        if cmd.new_commission.coefficient is not None:
            coefficient = CoefficientMapper.to_value_object(
                src=cmd.new_commission.coefficient,
            )

        current_rule: PaymentCommissionRule = await self._repo.get(cmd.method)
        new_rule = PaymentCommissionRuleFactory.create(
            method=cmd.method,
            coefficient=coefficient,
            tp=cmd.new_commission.type,
        )
        if new_rule == current_rule:
            return

        await self._repo.merge(old_rule=current_rule, new_rule=new_rule)
        await self._session.commit()
