from dataclasses import dataclass
from uuid import UUID

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.port import CategoryRepository
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import (
    PositionAccessService,
    PositionService,
)
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class RecoverPositionCmd:
    id: UUID


class RecoverPosition:
    def __init__(
        self,
        position_repo: PositionRepository,
        category_repo: CategoryRepository,
        session: DatabaseSession,
        current_user: GetCurrentUser,
        service: PositionService,
        clock: Clock,
    ):
        self._position_repo: PositionRepository = position_repo
        self._category_repo: CategoryRepository = category_repo
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._service: PositionService = service
        self._clock: Clock = clock

    async def __call__(self, cmd: RecoverPositionCmd) -> None:
        recoverer: User = await self._current_user()

        if not PositionAccessService.can_recover(
            recoverer_role=recoverer.role,
        ):
            raise PositionPermissionDenied

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        category: Category | None = await self._category_repo.get(
            category_id=position.category_id,
        )
        if category is None:
            raise DataCorruptionError(
                f"Position {position.id} exists but its category was not found",  # noqa: E501
            )
        self._service.recover(category=category, position=position)

        await self._session.commit()
