from decimal import Decimal

from app.common.port import DatabaseSession
from domain.common.coefficient import Coefficient
from domain.payment.enums import PaymentMethod
from domain.payment.exception import PaymentCommissionRuleNotCreated
from domain.payment.port import PaymentCommissionRuleRepository
from domain.payment.rule import ShopCommissionRule
from domain.referral.exception import ReferralPolicyNotCreated
from domain.referral.policy import ReferralPolicy
from domain.referral.port import ReferralPolicyRepository
from infra.common.bootstrap.default import (
    CATEGORY_SETTINGS,
    GENERAL_SETTINGS,
    PAYMENT_SETTINGS,
    POSITION_SETTINGS,
)
from presentation.aiogram.setting.category.exception import (
    CategorySettingsNotCreated,
)
from presentation.aiogram.setting.category.port import CategorySettingsGateway
from presentation.aiogram.setting.general.exception import (
    GeneralSettingsNotCreated,
)
from presentation.aiogram.setting.general.port import GeneralBotSettingsGateway
from presentation.aiogram.setting.payment.exception import (
    PaymentSettingsNotCreated,
)
from presentation.aiogram.setting.payment.port import PaymentSettingsGateway
from presentation.aiogram.setting.position.exception import (
    PositionSettingsNotCreated,
)
from presentation.aiogram.setting.position.port import PositionSettingsGateway


class Bootstrap:
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
        self._referral_policy_repo: ReferralPolicyRepository = (
            referral_policy_repo
        )
        self._payment_rule_repo: PaymentCommissionRuleRepository = (
            payment_rule_repo
        )
        self._session: DatabaseSession = session

    async def check(self) -> None:
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
            except PaymentCommissionRuleNotCreated:
                await self._payment_rule_repo.add(
                    rule=ShopCommissionRule(payment_method=method)
                )

    async def check_referral_policy(self) -> None:
        try:
            await self._referral_policy_repo.get()
        except ReferralPolicyNotCreated:
            await self._referral_policy_repo.add(
                policy=ReferralPolicy(
                    coefficient=Coefficient(value=Decimal("0.03"))
                )
            )

    async def check_position(self) -> None:
        try:
            await self._position_gateway.get()
        except PositionSettingsNotCreated:
            await self._position_gateway.save(settings=POSITION_SETTINGS)

    async def check_payment(self) -> None:
        try:
            await self._payment_settings_gw.get()
        except PaymentSettingsNotCreated:
            for settings in PAYMENT_SETTINGS:
                await self._payment_settings_gw.save(settings=settings)

    async def check_category(self) -> None:
        try:
            await self._category_settings_gw.get()
        except CategorySettingsNotCreated:
            await self._category_settings_gw.save(settings=CATEGORY_SETTINGS)

    async def check_general(self) -> None:
        try:
            await self._general_settings_gw.get()
        except GeneralSettingsNotCreated:
            await self._general_settings_gw.save(settings=GENERAL_SETTINGS)
