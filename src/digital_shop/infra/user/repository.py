from domain.user.entity import User
from domain.user.port import UserRepository
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.user import user_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, user: User) -> None:
        self._session.add(user)

    async def get(self, user_id: UserId) -> User | None:
        stmt = select(User).where(user_table.c.id == user_id.value).limit(1)
        result = await self._session.scalar(stmt)
        if not result:
            return None

        return result
