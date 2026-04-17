from dishka import Provider, Scope, provide, provide_all

from app.user.port import UserIdentifyResolver
from infra.authentication.telegram.adapter import (
    DefaultSuperAdminsProvider,
    TelegramContextGatewayImpl,
)
from infra.authentication.telegram.adapter.resolver import (
    TelegramIdentifyResolver,
)
from infra.authentication.telegram.handler import (
    DeactivateTelegramContext,
    EnsureTelegramContextHandler,
    UpdateTelegramCurrency,
    UpdateTelegramLangHandler,
)
from infra.authentication.telegram.port import (
    SuperAdminsProvider,
    TelegramContextGateway,
)


class TelegramAuthenticationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        provide(EnsureTelegramContextHandler),
        provide(UpdateTelegramLangHandler),
        provide(DeactivateTelegramContext),
        provide(UpdateTelegramCurrency),
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
