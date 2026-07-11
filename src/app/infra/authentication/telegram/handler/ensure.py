from dataclasses import dataclass
from zoneinfo import ZoneInfo

from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.user.service import UserApplicationService
from app.domain.common.money import Currency
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.port import UserRepository
from app.domain.user.value_object import UserId
from app.infra.authentication.telegram.dto import (
    TelegramContextData,
    TelegramContextDTO,
)
from app.infra.authentication.telegram.mapper import TelegramContextMapper
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import (
    SuperAdminsProvider,
    TelegramContextGateway,
)

_DEFAULT_ZONE_INFO = ZoneInfo("Europe/Moscow")


@dataclass(slots=True, frozen=True)
class EnsureTelegramContextData:
    tg_id: int

    tg_username: str | None
    tg_first_name: str

    referrer_tg_id: int | None


class EnsureTelegramContextHandler:
    def __init__(
        self,
        user_service: UserApplicationService,
        user_repo: UserRepository,
        gateway: TelegramContextGateway,
        session: DatabaseSession,
        admins: SuperAdminsProvider,
    ):
        self._session = session
        self._gateway = gateway
        self._admins = admins
        self._user_repo = user_repo
        self._user_service = user_service

    async def execute(
        self,
        data: EnsureTelegramContextData,
    ) -> TelegramContextDTO:
        ctx_data: TelegramContextData | None = await self._gateway.get_data(
            telegram_id=TelegramId(data.tg_id)
        )
        resolved_role = await self.__resolve_role(data=data)

        if not ctx_data:
            ctx_data = await self.__register(data=data, role=resolved_role)
            await self._gateway.save(ctx_data.ctx)

        else:
            ctx_data.ctx.sync_data(
                tg_first_name=data.tg_first_name, tg_username=data.tg_username
            )
            if resolved_role > ctx_data.role:
                user: User | None = await self._user_repo.get(
                    user_id=ctx_data.ctx.user_id
                )
                if not user:
                    raise DataCorruptionError

                user.system_assign_role(minimum_role=resolved_role)

        ctx = TelegramContextMapper.to_dto(src=ctx_data.ctx, role=ctx_data.role)

        await self._session.commit()

        return ctx

    async def __resolve_role(self, data: EnsureTelegramContextData) -> UserRole:
        super_admins: set[TelegramId] = await self._admins.get()
        return UserRole.SUPER_ADMIN if data.tg_id in super_admins else UserRole.USER

    async def __register(
        self,
        data: EnsureTelegramContextData,
        role: UserRole,
    ) -> TelegramContextData:
        referrer_id: UserId | None = None

        if data.referrer_tg_id is not None:
            referrer_id: UserId | None = await self._gateway.get_user_id(
                telegram_id=TelegramId(data.referrer_tg_id)
            )

        new_user: User = await self._user_service.register(
            role=role, referrer_id=referrer_id
        )

        ctx = TelegramContext(
            id=TelegramId(data.tg_id),
            user_id=new_user.id,
            tg_username=data.tg_username,
            tg_first_name=data.tg_first_name,
            lang=None,
            is_active=True,
            currency=Currency.RUB,
            timezone=_DEFAULT_ZONE_INFO,
        )
        return TelegramContextData(ctx=ctx, role=role)
