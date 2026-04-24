from dataclasses import dataclass

from app.common.exception import DataCorruptionError
from app.user.cmd import (
    RegisterUser,
    RegisterUserCmd,
)
from domain.common.money import Currency
from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.port import UserRepository
from domain.user.value_object import UserId
from infra.authentication.telegram.dto import (
    TelegramContextData,
    TelegramContextDTO,
)
from infra.authentication.telegram.mapper import TelegramContextMapper
from infra.authentication.telegram.model import TelegramContext, TelegramId
from infra.authentication.telegram.port import (
    NonExpiringSession,
    SuperAdminsProvider,
    TelegramContextGateway,
)


@dataclass(slots=True, frozen=True)
class EnsureTelegramContextData:
    tg_id: int

    tg_username: str | None
    tg_first_name: str

    referrer_tg_id: int | None


class EnsureTelegramContextHandler:
    def __init__(
        self,
        register_handler: RegisterUser,
        user_repo: UserRepository,
        gateway: TelegramContextGateway,
        session: NonExpiringSession,
        admins: SuperAdminsProvider,
    ):
        self._register: RegisterUser = register_handler
        self._session: NonExpiringSession = session
        self._gateway: TelegramContextGateway = gateway
        self._admins: SuperAdminsProvider = admins
        self._user_repo: UserRepository = user_repo

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

        await self._session.commit()

        return TelegramContextMapper.to_dto(
            src=ctx_data.ctx, role=ctx_data.role
        )

    async def __resolve_role(
        self, data: EnsureTelegramContextData
    ) -> UserRole:
        super_admins: set[TelegramId] = await self._admins.get()
        return (
            UserRole.SUPER_ADMIN
            if data.tg_id in super_admins
            else UserRole.USER
        )

    async def __register(
        self,
        data: EnsureTelegramContextData,
        role: UserRole,
    ) -> TelegramContextData:
        referrer_id: UserId | None = None

        if data.referrer_tg_id is not None:
            referrer_id = await self._gateway.get_user_id(
                telegram_id=TelegramId(data.referrer_tg_id)
            )

        new_user_id: UserId = await self._register(
            RegisterUserCmd(
                role=role,
                referrer_id=referrer_id.value if referrer_id else None,
            ),
        )
        ctx = TelegramContext(
            id=TelegramId(data.tg_id),
            user_id=new_user_id,
            tg_username=data.tg_username,
            tg_first_name=data.tg_first_name,
            lang=None,
            is_active=True,
            currency=Currency.RUB,
        )
        return TelegramContextData(ctx=ctx, role=role)
