from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.category.exception import CategoryNotFound
from app.user.service import GetCurrentUser
from domain.common.localized import Language
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryAccessService
from domain.product.category.value_object import CategoryId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class SetCategoryNameCmd:
    id: UUID
    name: str
    lang: Language


class SetCategoryName:
    def __init__(
        self,
        repository: CategoryRepository,
        current_user: GetCurrentUser,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._repository: CategoryRepository = repository
        self._current_user: GetCurrentUser = current_user
        self._session: DatabaseSession = session
        self._clock: Clock = clock

    async def __call__(self, cmd: SetCategoryNameCmd) -> None:
        editor: User = await self._current_user()

        if not CategoryAccessService.can_edit(editor=editor):
            raise CategoryAccessDenied

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFound

        category.set_name(name=cmd.name, now=self._clock.now(), lang=cmd.lang)

        await self._session.commit()
