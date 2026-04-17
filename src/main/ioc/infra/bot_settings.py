from adaptix import Retort
from dishka import Provider, Scope, provide, provide_all
from redis.asyncio import Redis

from infra.presentation.aiogram.bot_settings.category_gateway import (
    CategorySettingsGatewayImpl,
)
from infra.presentation.aiogram.bot_settings.general_gateway import (
    GeneralBotSettingsGatewayImpl,
)
from infra.presentation.aiogram.bot_settings.payment_gateway import (
    PaymentSettingsGatewayImpl,
)
from infra.presentation.aiogram.bot_settings.position_gateway import (
    PositionSettingsGatewayImpl,
)
from main.ioc.tp import BotId
from presentation.aiogram.setting.category.cmd import (
    ChangeCategoryDefaultLang,
    SwitchWithNoItemsCategory,
)
from presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)
from presentation.aiogram.setting.general.handler import (
    SetSupportUsername,
    SwitchTechWorkStatus,
)
from presentation.aiogram.setting.general.port import (
    GeneralBotSettingsGateway,
)
from presentation.aiogram.setting.payment.cmd import (
    SwitchPaymentSettingStatus,
)
from presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)
from presentation.aiogram.setting.position.cmd import (
    ChangePositionDefaultCurrency,
    ChangePositionDefaultLang,
    SwitchShowPositionWithNoItems,
)
from presentation.aiogram.setting.position.port import PositionSettingsGateway


class BotSettingsAdaptersProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_general_gateway(
        self,
        retort: Retort,
        bot_id: BotId,
        redis: Redis,
    ) -> GeneralBotSettingsGateway:
        return GeneralBotSettingsGatewayImpl(redis, retort, bot_id)

    @provide(scope=Scope.APP)
    async def get_category_gateway(
        self,
        retort: Retort,
        bot_id: BotId,
        redis: Redis,
    ) -> CategorySettingsGateway:
        return CategorySettingsGatewayImpl(redis, retort, bot_id)

    @provide(scope=Scope.APP)
    async def get_payment_settings_gateway(
        self,
        retort: Retort,
        bot_id: BotId,
        redis: Redis,
    ) -> PaymentSettingsGateway:
        return PaymentSettingsGatewayImpl(
            redis=redis,
            retort=retort,
            bot_id=bot_id,
        )

    @provide(scope=Scope.APP)
    async def get_position_settings_gateway(
        self,
        retort: Retort,
        bot_id: BotId,
        redis: Redis,
    ) -> PositionSettingsGateway:
        return PositionSettingsGatewayImpl(
            redis=redis,
            retort=retort,
            bot_id=bot_id,
        )

    payment_handlers = provide_all(
        provide(SwitchPaymentSettingStatus, scope=Scope.REQUEST),
        scope=Scope.REQUEST,
    )

    general_handlers = provide_all(
        provide(SwitchTechWorkStatus, scope=Scope.REQUEST),
        provide(SetSupportUsername, scope=Scope.REQUEST),
        scope=Scope.REQUEST,
    )

    category_handlers = provide_all(
        provide(SwitchWithNoItemsCategory, scope=Scope.REQUEST),
        provide(ChangeCategoryDefaultLang, scope=Scope.REQUEST),
        scope=Scope.REQUEST,
    )

    position_settings = provide_all(
        provide(SwitchShowPositionWithNoItems, scope=Scope.REQUEST),
        provide(ChangePositionDefaultLang, scope=Scope.REQUEST),
        provide(ChangePositionDefaultCurrency, scope=Scope.REQUEST),
        scope=Scope.REQUEST,
    )
