from aiogram.types import TelegramObject
from aiogram.types import User as AioUser
from app.user.port import UserIdentifyProvider
from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.authentication.telegram.handler import (
    EnsureTelegramContextData,
    EnsureTelegramContextHandler,
)
from infra.presentation.aiogram.broadcast.broadcaster import (
    TelegramBroadcasterImpl,
)
from infra.presentation.aiogram.broadcast.kb_builder import (
    BroadcastKeyboardBuilder,
)
from infra.presentation.aiogram.broadcast.limiter import BroadcastRateLimiter
from infra.presentation.aiogram.broadcast.progress import (
    BroadcastProgressGateway,
    BroadcastProgressMessage,
)
from infra.presentation.aiogram.broadcast.progress.message import (
    BroadcastProgressConfig,
)
from infra.text.text import FluentTranslatorHub
from presentation.aiogram.adapter.idp import AiogramUserIdentifyProvider
from presentation.aiogram.kb import ServiceKeyboard
from presentation.aiogram.mapper import FileKeyMapper
from presentation.aiogram.mapper.file import FileDTOFactory, FileSender
from presentation.aiogram.port import Text, TranslatorHub
from presentation.aiogram.port.broadcast import TelegramBroadcaster
from presentation.aiogram.referral import extract_ref_deeplink
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)
from presentation.aiogram.setting.general.model import GeneralBotSettings
from presentation.aiogram.setting.general.port import (
    GeneralBotSettingsGateway,
)
from presentation.aiogram.setting.position.model import PositionSettings
from presentation.aiogram.setting.position.port import PositionSettingsGateway
from redis.asyncio import Redis


class AiogramAdaptersProvider(Provider):
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

    idp = provide(
        AiogramUserIdentifyProvider,
        provides=UserIdentifyProvider,
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

    broadcast_progress_gateway = provide(
        BroadcastProgressGateway, scope=Scope.APP
    )

    broadcast_progress_message = provide(
        BroadcastProgressMessage, scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    async def get_progress_config(self) -> BroadcastProgressConfig:
        return BroadcastProgressConfig()

    @provide(scope=Scope.APP)
    async def get_broadcast_limiter(
        self, redis: Redis
    ) -> BroadcastRateLimiter:
        return BroadcastRateLimiter(redis=redis)

    broadcast_keyboard_builder = provide(
        BroadcastKeyboardBuilder, scope=Scope.APP
    )

    broadcaster = provide(
        TelegramBroadcasterImpl, provides=TelegramBroadcaster, scope=Scope.APP
    )
