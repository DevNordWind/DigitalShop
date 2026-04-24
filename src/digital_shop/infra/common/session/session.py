import logging
from collections.abc import Sequence

from app.common.port import DatabaseSession
from infra.common.session.mapper import IntegrityErrorMapper
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class DatabaseSessionImpl(DatabaseSession):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except IntegrityError as e:
            constraint: str | None = getattr(
                e.orig.diag,  # type: ignore[union-attr]
                "constraint_name",
                None,
            )
            if constraint:
                domain_error = IntegrityErrorMapper.to_domain(constraint)
                if not domain_error:
                    logger.error(
                        "Unmapped DB constraint violated: %s - %s",
                        constraint,
                        str(e),
                    )
                    raise e
                raise domain_error from e

    async def flush(self, objects: Sequence[object] | None = None) -> None:
        await self._session.flush(objects)

    async def rollback(self) -> None:
        await self._session.rollback()
