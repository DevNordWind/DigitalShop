from decimal import Decimal

from app.app.common.port.session import DatabaseSession
from app.app.payment.exception import PaymentCommissionRuleNotCreatedError
from app.app.referral.exception import ReferralPolicyNotCreatedError
from app.domain.common.coefficient import Coefficient
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.port import PaymentCommissionRuleRepository
from app.domain.payment.rule import ShopCommissionRule
from app.domain.referral.policy import ReferralPolicy
from app.domain.referral.port import ReferralPolicyRepository
from app.infra.common.bootstrap.entities.default import (
    CATEGORY_SETTINGS,
    GENERAL_SETTINGS,
    PAYMENT_SETTINGS,
    POSITION_SETTINGS,
)
from app.presentation.aiogram.setting.category import (
    CategorySettingsGateway,
    CategorySettingsNotCreatedError,
)
from app.presentation.aiogram.setting.general import (
    GeneralBotSettingsGateway,
    GeneralSettingsNotCreatedError,
)
from app.presentation.aiogram.setting.payment import (
    PaymentSettingsGateway,
    PaymentSettingsNotCreatedError,
)
from app.presentation.aiogram.setting.position import (
    PositionSettingsGateway,
    PositionSettingsNotCreatedError,
)


class DefaultEntitiesBootstrap:
    def __init__(
        self,
        general_settings_gateway: GeneralBotSettingsGateway,
        category_settings_gateway: CategorySettingsGateway,
        payment_settings_gateway: PaymentSettingsGateway,
        position_gateway: PositionSettingsGateway,
        referral_policy_repo: ReferralPolicyRepository,
        payment_rule_repo: PaymentCommissionRuleRepository,
        session: DatabaseSession,
    ):
        self._general_settings_gw = general_settings_gateway
        self._category_settings_gw = category_settings_gateway
        self._payment_settings_gw = payment_settings_gateway
        self._position_gateway: PositionSettingsGateway = position_gateway
        self._referral_policy_repo: ReferralPolicyRepository = referral_policy_repo
        self._payment_rule_repo: PaymentCommissionRuleRepository = payment_rule_repo
        self._session: DatabaseSession = session

    async def startup(self) -> None:
        await self.check_general()
        await self.check_category()
        await self.check_payment()
        await self.check_position()
        await self.check_referral_policy()
        await self.check_payment_rule()

        await self._session.commit()

    async def check_payment_rule(self) -> None:
        for method in PaymentMethod:
            try:
                await self._payment_rule_repo.get(method=method)
            except PaymentCommissionRuleNotCreatedError:
                await self._payment_rule_repo.add(
                    rule=ShopCommissionRule(payment_method=method)
                )

    async def check_referral_policy(self) -> None:
        try:
            await self._referral_policy_repo.get()
        except ReferralPolicyNotCreatedError:
            await self._referral_policy_repo.add(
                policy=ReferralPolicy(coefficient=Coefficient(value=Decimal("0.03")))
            )

    async def check_position(self) -> None:
        try:
            await self._position_gateway.get()
        except PositionSettingsNotCreatedError:
            await self._position_gateway.save(settings=POSITION_SETTINGS)

    async def check_payment(self) -> None:
        try:
            await self._payment_settings_gw.get()
        except PaymentSettingsNotCreatedError:
            for settings in PAYMENT_SETTINGS:
                await self._payment_settings_gw.save(settings=settings)

    async def check_category(self) -> None:
        try:
            await self._category_settings_gw.get()
        except CategorySettingsNotCreatedError:
            await self._category_settings_gw.save(settings=CATEGORY_SETTINGS)

    async def check_general(self) -> None:
        try:
            await self._general_settings_gw.get()
        except GeneralSettingsNotCreatedError:
            await self._general_settings_gw.save(settings=GENERAL_SETTINGS)
