from dataclasses import dataclass

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession
from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.payment.port.payment import CreateInvoice, Invoice
from app.user.service import GetCurrentUser
from domain.common.money import Money
from domain.common.port import Clock
from domain.payment.enums import PaymentMethod, PaymentPurposeType
from domain.payment.port import (
    PaymentCommissionRuleRepository,
    PaymentRepository,
)
from domain.payment.rule import PaymentCommissionRule
from domain.payment.service import PaymentService
from domain.payment.value_object import PaymentExternalId, PaymentPurpose
from domain.user.entity import User
from domain.wallet.entity import Wallet
from domain.wallet.exception import WalletPermissionDenied
from domain.wallet.port import WalletRepository
from domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class CreateTopUpPaymentCmd:
    amount: MoneyDTO
    method: PaymentMethod


class CreateTopUpPayment:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        payment_repo: PaymentRepository,
        rule_repo: PaymentCommissionRuleRepository,
        payment_service: PaymentService,
        payment_factory: PaymentMethodGatewayFactory,
        current_user: GetCurrentUser,
        clock: Clock,
        session: DatabaseSession,
    ):
        self._wallet_repo: WalletRepository = wallet_repo
        self._payment_repo: PaymentRepository = payment_repo
        self._rule_repo: PaymentCommissionRuleRepository = rule_repo
        self._payment_service: PaymentService = payment_service
        self._payment_factory: PaymentMethodGatewayFactory = payment_factory
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock
        self._session: DatabaseSession = session

    async def __call__(self, cmd: CreateTopUpPaymentCmd) -> Invoice:
        creator: User = await self._current_user()
        if not WalletAccessService.can_top_up_payment(
            actor_user_id=creator.id,
            actor_role=creator.role,
            wallet_user_id=creator.id,
        ):
            raise WalletPermissionDenied

        amount: Money = MoneyMapper.to_value_object(src=cmd.amount)
        wallet: (
            Wallet | None
        ) = await self._wallet_repo.get_by_currency_for_update(
            user_id=creator.id,
            currency=amount.currency,
        )
        if not wallet:
            raise DataCorruptionError(
                f"User {creator.id} exists but its wallet was not found",
            )

        wallet.ensure_can_top_up(amount=amount)
        rule: PaymentCommissionRule = await self._rule_repo.get(
            method=cmd.method,
        )
        payment = self._payment_service.create(
            creator=creator,
            purpose=PaymentPurpose(
                reference_id=wallet.id.value,
                type=PaymentPurposeType.WALLET_TOP_UP,
            ),
            method=cmd.method,
            amount=amount,
            commission_rule=rule,
        )
        await self._payment_repo.add(payment)

        try:
            gateway: PaymentMethodGateway = await self._payment_factory.get(
                method=payment.method,
            )
            invoice: Invoice = await gateway.create(
                data=CreateInvoice(
                    payment_id=payment.id.value,
                    to_pay=MoneyMapper.to_dto(src=payment.to_pay),
                ),
            )
            payment.start(
                external_id=PaymentExternalId(invoice.invoice_id),
                now=self._clock.now(),
            )
        except PaymentMethodGatewayError as e:
            payment.fail(now=self._clock.now())
            await self._session.commit()
            raise e

        await self._session.commit()
        return invoice
