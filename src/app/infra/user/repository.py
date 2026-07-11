from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entity import User
from app.domain.user.port import UserRepository
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.user import user_table


class SqlAUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, user: User) -> None:
        self._session.add(user)

    @override
    async def get(self, user_id: UserId) -> User | None:
        stmt = select(User).where(user_table.c.id == user_id).limit(1)
        return await self._session.scalar(stmt)
