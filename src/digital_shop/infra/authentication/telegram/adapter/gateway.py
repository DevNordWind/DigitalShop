from collections.abc import Sequence

from domain.common.localized import Language
from domain.user.enums import UserRole
from domain.user.value_object import UserId
from infra.authentication.telegram.adapter.session import (
    NonExpiringAsyncSession,
)
from infra.authentication.telegram.dto import TelegramContextData
from infra.authentication.telegram.model import TelegramContext, TelegramId
from infra.authentication.telegram.port import TelegramContextGateway
from infra.framework.sql_alchemy.table.telegram_context import (
    telegram_context_table,
)
from infra.framework.sql_alchemy.table.user import user_table
from sqlalchemy import select


class TelegramContextGatewayImpl(TelegramContextGateway):
    def __init__(self, session: NonExpiringAsyncSession):
        self._session: NonExpiringAsyncSession = session

    async def save(self, context: TelegramContext) -> None:
        self._session.add(context)

    async def get_data(
        self, telegram_id: TelegramId
    ) -> TelegramContextData | None:
        stmt = (
            select(TelegramContext, user_table.c.role)
            .where(
                telegram_context_table.c.id == telegram_id,
            )
            .join(
                user_table, user_table.c.id == telegram_context_table.c.user_id
            )
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return TelegramContextData(ctx=row[0], role=row[1])

    async def get(self, telegram_id: TelegramId) -> TelegramContext | None:
        stmt = select(TelegramContext).where(
            telegram_context_table.c.id == telegram_id,
        )
        result: TelegramContext | None = await self._session.scalar(stmt)

        return result or None

    async def get_by_user_id(self, user_id: UserId) -> TelegramContext | None:
        stmt = select(TelegramContext).where(
            telegram_context_table.c.user_id == user_id.value,
        )
        result = await self._session.scalar(stmt)

        return result or None

    async def get_user_id(self, telegram_id: TelegramId) -> UserId | None:
        stmt = select(telegram_context_table.c.user_id).where(
            telegram_context_table.c.id == telegram_id
        )
        result = await self._session.scalar(stmt)
        if not result:
            return None

        return UserId(result)

    async def get_lang(self, telegram_id: TelegramId) -> Language | None:
        stmt = select(telegram_context_table.c.lang).where(
            telegram_context_table.c.id == telegram_id
        )
        result = await self._session.scalar(stmt)

        return result or None

    async def get_admins(
        self,
        is_active: bool | None = None,
    ) -> list[TelegramContext]:
        stmt = (
            select(TelegramContext)
            .where(
                user_table.c.role.in_((UserRole.ADMIN, UserRole.SUPER_ADMIN)),
            )
            .join(
                user_table, telegram_context_table.c.user_id == user_table.c.id
            )
        )

        if is_active is not None:
            stmt = stmt.where(
                telegram_context_table.c.is_active.is_(is_active),
            )

        result = (await self._session.scalars(stmt)).all()

        return list(result)

    async def get_all(
        self,
        is_active: bool | None = None,
    ) -> list[TelegramContext]:
        stmt = select(TelegramContext)
        if is_active is not None:
            stmt = stmt.where(
                telegram_context_table.c.is_active.is_(is_active),
            )
        result = (await self._session.scalars(stmt)).all()

        return list(result)

    async def get_all_by_langs(
        self, langs: Sequence[Language], is_active: bool | None = None
    ) -> list[TelegramContext]:
        stmt = select(TelegramContext).where(
            telegram_context_table.c.lang.in_(langs)
        )
        if is_active is not None:
            stmt = stmt.where(
                telegram_context_table.c.is_active.is_(is_active),
            )
        result = (await self._session.scalars(stmt)).all()

        return list(result)
