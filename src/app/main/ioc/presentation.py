from adaptix import Retort
from aiogram.types import TelegramObject
from aiogram.types import User as AioUser
from dishka import Provider, Scope, provide, provide_all
from dishka.integrations.aiogram import AiogramMiddlewareData
from redis.asyncio import Redis

from app.app.common.port.actor_provider import ActorProvider
from app.app.user.port import UserIdentifyResolver
from app.infra.authentication.telegram.adapter import (
    DefaultSuperAdminsProvider,
    TelegramContextGatewayImpl,
)
from app.infra.authentication.telegram.adapter.resolver import (
    TelegramIdentifyResolver,
)
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.handler import (
    DeactivateTelegramContext,
    EnsureTelegramContextData,
    EnsureTelegramContextHandler,
    UpdateTelegramCurrency,
    UpdateTelegramLangHandler,
)
from app.infra.authentication.telegram.port import (
    SuperAdminsProvider,
    TelegramContextGateway,
)
from app.infra.presentation.aiogram import (
    FileKeyMapper,
    FluentTranslatorHub,
    RedisCategorySettingsGateway,
    RedisGeneralBotSettingsGateway,
    RedisPaymentSettingsGateway,
    RedisPositionSettingsGateway,
)
from app.infra.presentation.aiogram.broadcast.broadcaster import (
    TelegramBroadcasterImpl,
)
from app.infra.presentation.aiogram.broadcast.kb_builder import (
    BroadcastKeyboardBuilder,
)
from app.infra.presentation.aiogram.broadcast.limiter import BroadcastRateLimiter
from app.infra.presentation.aiogram.broadcast.progress import (
    BroadcastProgressGateway,
    BroadcastProgressMessage,
)
from app.infra.presentation.aiogram.broadcast.progress.message import (
    BroadcastProgressConfig,
)
from app.infra.presentation.aiogram.mapper import FileDTOFactory, FileSender
from app.presentation.aiogram.adapter import AiogramActorProvider
from app.presentation.aiogram.kb import ServiceKeyboard
from app.presentation.aiogram.port import Text, TranslatorHub
from app.presentation.aiogram.port.broadcast import TelegramBroadcaster
from app.presentation.aiogram.referral import extract_ref_deeplink
from app.presentation.aiogram.setting.category import (
    ChangeCategoryDefaultLang,
    SwitchWithNoItemsCategory,
)
from app.presentation.aiogram.setting.category.model import CategorySettings
from app.presentation.aiogram.setting.category.port import CategorySettingsGateway
from app.presentation.aiogram.setting.general import (
    SetSupportUsername,
    SwitchTechWorkStatus,
)
from app.presentation.aiogram.setting.general.model import GeneralBotSettings
from app.presentation.aiogram.setting.general.port import GeneralBotSettingsGateway
from app.presentation.aiogram.setting.payment import (
    PaymentSettingsGateway,
    SwitchPaymentSettingStatus,
)
from app.presentation.aiogram.setting.position import (
    ChangePositionDefaultCurrency,
    ChangePositionDefaultLang,
    SwitchShowPositionWithNoItems,
)
from app.presentation.aiogram.setting.position.model import PositionSettings
from app.presentation.aiogram.setting.position.port import PositionSettingsGateway
from app.presentation.aiogram.util.error_translator import (
    ErrorTranslator,
    ErrorTranslatorConfig,
)


class AiogramAdaptersProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_general_settings_gw(
        self, redis: Redis, retort: Retort
    ) -> GeneralBotSettingsGateway:
        return RedisGeneralBotSettingsGateway(redis=redis, retort=retort)

    @provide(scope=Scope.APP)
    async def get_position_settings_gw(
        self, redis: Redis, retort: Retort
    ) -> PositionSettingsGateway:
        return RedisPositionSettingsGateway(redis, retort)

    @provide(scope=Scope.APP)
    async def get_category_settings_gw(self, redis: Redis) -> CategorySettingsGateway:
        return RedisCategorySettingsGateway(redis)

    @provide(scope=Scope.APP)
    async def get_payment_settings_gw(
        self, redis: Redis, retort: Retort
    ) -> PaymentSettingsGateway:
        return RedisPaymentSettingsGateway(redis, retort)

    @provide(scope=Scope.REQUEST)
    async def get_aio_user(
        self,
        middleware_data: AiogramMiddlewareData,
    ) -> AioUser:
        return middleware_data["event_from_user"]  # type: ignore[no-any-return]

    @provide(scope=Scope.REQUEST)
    async def get_context(
        self,
        event: TelegramObject,
        aio_user: AioUser,
        handler: EnsureTelegramContextHandler,
    ) -> TelegramContextDTO:
        return await handler.execute(
            data=EnsureTelegramContextData(
                tg_id=aio_user.id,
                tg_username=aio_user.username,
                tg_first_name=aio_user.first_name,
                referrer_tg_id=extract_ref_deeplink(event=event),
            )
        )

    actor_provider = provide(
        AiogramActorProvider,
        provides=ActorProvider,
        scope=Scope.REQUEST,
    )

    file_factory = provide(FileDTOFactory, scope=Scope.APP)

    file_mapper = provide(FileKeyMapper, scope=Scope.APP)

    file_sender = provide(FileSender, scope=Scope.APP)

    service_keyboard = provide(ServiceKeyboard, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    async def get_t_hub(self) -> TranslatorHub:
        return FluentTranslatorHub()

    @provide(scope=Scope.REQUEST)
    async def get_text(
        self,
        t_hub: TranslatorHub,
        ctx: TelegramContextDTO,
    ) -> Text:
        return t_hub(ctx.lang)

    @provide(scope=Scope.REQUEST)
    async def get_general_settings(
        self,
        gateway: GeneralBotSettingsGateway,
    ) -> GeneralBotSettings:
        return await gateway.get()

    @provide(scope=Scope.REQUEST)
    async def get_category_settings(
        self,
        gateway: CategorySettingsGateway,
    ) -> CategorySettings:
        return await gateway.get()

    @provide(scope=Scope.REQUEST)
    async def get_position_settings(
        self,
        gateway: PositionSettingsGateway,
    ) -> PositionSettings:
        return await gateway.get()

    broadcast_progress_gateway = provide(BroadcastProgressGateway, scope=Scope.APP)

    broadcast_progress_message = provide(BroadcastProgressMessage, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_progress_config(self) -> BroadcastProgressConfig:
        return BroadcastProgressConfig()

    @provide(scope=Scope.APP)
    async def get_broadcast_limiter(self, redis: Redis) -> BroadcastRateLimiter:
        return BroadcastRateLimiter(redis=redis)

    broadcast_keyboard_builder = provide(BroadcastKeyboardBuilder, scope=Scope.APP)

    broadcaster = provide(
        TelegramBroadcasterImpl, provides=TelegramBroadcaster, scope=Scope.APP
    )

    @provide(scope=Scope.REQUEST)
    async def get_error_translator(self, text: Text) -> ErrorTranslator:
        return ErrorTranslator(text=text, config=ErrorTranslatorConfig())

    commands = provide_all(
        ChangePositionDefaultCurrency,
        ChangePositionDefaultLang,
        SwitchShowPositionWithNoItems,
        SwitchPaymentSettingStatus,
        SetSupportUsername,
        SwitchTechWorkStatus,
        ChangeCategoryDefaultLang,
        SwitchWithNoItemsCategory,
        scope=Scope.REQUEST,
    )


class TelegramAuthenticationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        EnsureTelegramContextHandler,
        UpdateTelegramLangHandler,
        DeactivateTelegramContext,
        UpdateTelegramCurrency,
    )

    admins = provide(
        DefaultSuperAdminsProvider,
        provides=SuperAdminsProvider,
        scope=Scope.APP,
    )

    idr = provide(
        TelegramIdentifyResolver,
        provides=UserIdentifyResolver,
    )

    gateway = provide(
        TelegramContextGatewayImpl,
        provides=TelegramContextGateway,
    )
