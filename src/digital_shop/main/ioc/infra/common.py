import uuid
from collections.abc import AsyncIterable

from adaptix import Retort
from app.common.port import DatabaseSession, Translator
from app.common.port.file_storage import FileStorageReader, FileStorageSession
from app.common.port.telegram_notification import TelegramNotification
from config.file import FileStorageConfig
from dishka import Provider, Scope, provide
from domain.common.exchange_rate import ExchangeRateGateway
from domain.common.port import Clock, UUIDProvider
from infra.common.bootstrap import Bootstrap
from infra.common.clock import SystemClock
from infra.common.file_storage.reader import FileSystemReader
from infra.common.file_storage.session.session import FileSystemStorageSession
from infra.common.file_storage.session.writer import FileSystemWriter
from infra.common.rate_gateway import (
    CryptoPayExchangeRateGateway,
    CryptoPayRateLoader,
    ExchangeRateCache,
)
from infra.common.session import DatabaseSessionImpl
from infra.common.telegram_notification import (
    NotificationKeyboardBuilder,
    NotificationTextBuilder,
    TelegramNotificationImpl,
)
from infra.common.translator import UnofficialGoogleTranslator
from redis.asyncio import Redis


class CommonAdaptersProvider(Provider):
    scope = Scope.APP

    clock = provide(SystemClock, provides=Clock)

    session = provide(
        DatabaseSessionImpl,
        provides=DatabaseSession,
        scope=Scope.REQUEST,
    )

    translator = provide(
        UnofficialGoogleTranslator,
        provides=Translator,
        scope=Scope.APP,
    )

    @provide
    async def get_uuid_provider(self) -> UUIDProvider:
        return uuid.uuid7

    kb_builder = provide(NotificationKeyboardBuilder)
    text_builder = provide(NotificationTextBuilder)

    telegram_notification = provide(
        TelegramNotificationImpl,
        provides=TelegramNotification,
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    async def get_file_writer(
        self,
        config: FileStorageConfig,
    ) -> FileSystemWriter:
        return FileSystemWriter(base_path=config.base_path)

    @provide(scope=Scope.APP)
    async def get_file_reader(
        self,
        config: FileStorageConfig,
    ) -> FileStorageReader:
        return FileSystemReader(base_path=config.base_path)

    @provide(scope=Scope.REQUEST)
    async def get_file_session(
        self,
        writer: FileSystemWriter,
    ) -> AsyncIterable[FileStorageSession]:
        async with FileSystemStorageSession(writer=writer) as session:
            yield session

    rate_loader = provide(CryptoPayRateLoader, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_rate_cache(
        self,
        redis: Redis,
        retort: Retort,
    ) -> ExchangeRateCache:
        return ExchangeRateCache(redis=redis, retort=retort)

    @provide(scope=Scope.APP)
    async def get_rate_gateway(
        self,
        loader: CryptoPayRateLoader,
        cache: ExchangeRateCache,
        clock: Clock,
    ) -> ExchangeRateGateway:
        return CryptoPayExchangeRateGateway(
            loader=loader,
            cache=cache,
            clock=clock,
        )

    bootstrap = provide(Bootstrap, scope=Scope.REQUEST)
