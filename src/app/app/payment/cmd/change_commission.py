from dataclasses import dataclass

from app.app.common.dto.coefficient import CoefficientMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.payment.dto.commission import CommissionDTO
from app.domain.common.coefficient import Coefficient
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.factory import PaymentCommissionRuleFactory
from app.domain.payment.port import PaymentCommissionRuleRepository
from app.domain.payment.rule import PaymentCommissionRule
from app.domain.payment.service import PaymentCommissionRuleAccessService


@dataclass(slots=True, frozen=True)
class ChangePaymentCommissionCoefficientCmd:
    method: PaymentMethod
    new_commission: CommissionDTO


class ChangePaymentCommissionCoefficient:
    def __init__(
        self,
        repo: PaymentCommissionRuleRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
    ):
        self._repo: PaymentCommissionRuleRepository = repo
        self._actor_provider = actor_provider
        self._session: DatabaseSession = session

    async def __call__(
        self,
        cmd: ChangePaymentCommissionCoefficientCmd,
    ) -> None:
        PaymentCommissionRuleAccessService.ensure_can_change(
            actor=await self._actor_provider.get()
        )

        coefficient: Coefficient | None = None

        if cmd.new_commission.coefficient is not None:
            coefficient = CoefficientMapper.to_value_object(
                src=cmd.new_commission.coefficient,
            )

        current_rule: PaymentCommissionRule = await self._repo.get(method=cmd.method)
        new_rule = PaymentCommissionRuleFactory.create(
            method=cmd.method,
            coefficient=coefficient,
            tp=cmd.new_commission.type,
        )
        if new_rule == current_rule:
            return

        await self._repo.merge(old_rule=current_rule, new_rule=new_rule)
        await self._session.commit()
