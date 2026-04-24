from typing import NewType

from sqlalchemy.ext.asyncio import AsyncSession

NonExpiringAsyncSession = NewType("NonExpiringAsyncSession", AsyncSession)
