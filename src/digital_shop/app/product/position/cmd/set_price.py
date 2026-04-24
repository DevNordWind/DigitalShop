from dataclasses import dataclass
from uuid import UUID

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.port import DatabaseSession
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class SetPositionPriceCmd:
    id: UUID
    money: MoneyDTO


class SetPositionPrice:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(self, cmd: SetPositionPriceCmd) -> None:
        price = MoneyMapper.to_value_object(src=cmd.money)

        editor: User = await self._current_user()

        if not PositionAccessService.can_edit(editor_role=editor.role):
            raise PositionPermissionDenied

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        position.set_price(price=price, now=self._clock.now())

        await self._session.commit()
