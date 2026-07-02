from collections.abc import AsyncIterable

import orjson
from adaptix import Retort
from aiocryptopay import AioCryptoPay  # type: ignore[import-untyped]
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
)
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import (
    AiogramProvider as DefaultAiogramProvider,
)
from googletrans import Translator  # type: ignore[import-untyped]
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from taskiq import AsyncBroker, ScheduleSource

from app.app.common.port.actor_provider import ActorProvider
from app.config import DatabaseConfig, PaymentConfig, RedisConfig
from app.config.bot import BotConfig
from app.infra.framework.adaptix import (
    get_exchange_rate_recipe,
    get_media_attachment_recipe,
)
from app.infra.framework.taskiq import (
    TaskIqActorProvider,
    get_broker,
    get_priority_broker,
    get_schedule_source,
)
from app.infra.framework.taskiq.tp import PriorityBroker
from app.presentation.aiogram.dp import make_dispatcher


class RetortProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_retort(self) -> Retort:
        return Retort(
            strict_coercion=False,
            recipe=get_media_attachment_recipe() + get_exchange_rate_recipe(),
        )


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, configuration: DatabaseConfig) -> AsyncEngine:
        return create_async_engine(
            url=configuration.connection_str,
            echo=configuration.sql_alchemy.echo,
            hide_parameters=configuration.sql_alchemy.hide_parameters,
            pool_pre_ping=configuration.sql_alchemy.pool_pre_ping,
            max_overflow=configuration.sql_alchemy.max_overflow,
            pool_size=configuration.sql_alchemy.pool_size,
            json_serializer=lambda obj: orjson.dumps(obj).decode(),
            json_deserializer=orjson.loads,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        engine: AsyncEngine,
    ) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(engine) as session:
            yield session


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, configuration: RedisConfig) -> Redis:
        return Redis(
            db=configuration.db,
            host=configuration.host,
            username=configuration.username,
            password=configuration.password,
            port=configuration.port,
            decode_responses=True,
        )


class AiogramProvider(DefaultAiogramProvider):
    @provide(scope=Scope.APP)
    async def get_key_builder(self) -> KeyBuilder:
        return DefaultKeyBuilder(with_bot_id=True, with_destiny=True)

    @provide(scope=Scope.APP)
    async def get_storage(
        self,
        redis: Redis,
        key_builder: KeyBuilder,
    ) -> BaseStorage:
        return RedisStorage(
            redis=redis,
            key_builder=key_builder,
            json_loads=orjson.loads,
            json_dumps=lambda obj: orjson.dumps(obj).decode(),
        )

    @provide(scope=Scope.APP)
    async def get_bot(self, config: BotConfig) -> Bot:
        return Bot(
            token=config.token,
            session=AiohttpSession(
                json_loads=orjson.loads,
                json_dumps=lambda obj: orjson.dumps(obj).decode(),
            ),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    @provide(scope=Scope.APP)
    async def get_events_isolation(
        self, redis: Redis, key_builder: KeyBuilder
    ) -> BaseEventIsolation:
        return RedisEventIsolation(redis, key_builder)

    @provide(scope=Scope.APP)
    async def get_dp(
        self,
        storage: BaseStorage,
        events_isolation: BaseEventIsolation,
    ) -> Dispatcher:
        return make_dispatcher(storage, events_isolation)


class GoogleTranslatorProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_translator(self) -> AsyncIterable[Translator]:
        translator = Translator()
        try:
            yield translator
        finally:
            await translator.client.aclose()


class TaskIqProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_broker(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[AsyncBroker]:
        broker = get_broker(redis_config=config)
        await broker.startup()
        try:
            yield broker
        finally:
            await broker.shutdown()

    @provide
    async def get_priority_broker(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[PriorityBroker]:
        broker = get_priority_broker(redis_config=config)
        await broker.startup()
        try:
            yield broker
        finally:
            await broker.shutdown()

    @provide
    async def get_schedule_source(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[ScheduleSource]:
        source = get_schedule_source(redis_config=config)
        await source.startup()
        try:
            yield source
        finally:
            await source.shutdown()


class TaskIqActorProvider(Provider):
    scope = Scope.APP

    actor_provider = provide(TaskIqActorProvider, provides=ActorProvider)


class CryptoBotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_crypto_bot(
        self,
        config: PaymentConfig,
    ) -> AsyncIterable[AioCryptoPay]:
        crypto_pay = AioCryptoPay(
            token=config.crypto_pay.token,
            network=config.crypto_pay.network,
        )
        try:
            yield crypto_pay
        finally:
            await crypto_pay.close()
