from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.localized import Language
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId


@dataclass(slots=True, frozen=True)
class ChangeCategoryNameDefaultLangCmd:
    id: UUID
    lang: Language


class ChangeCategoryNameDefaultLang:
    def __init__(
        self,
        repository: CategoryRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._repository = repository
        self._actor_provider = actor_provider
        self._session = session
        self._clock = clock

    async def __call__(
        self,
        cmd: ChangeCategoryNameDefaultLangCmd,
    ) -> None:
        CategoryAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        category.change_name_default_lang(
            lang=cmd.lang,
            now=self._clock.now(),
        )

        await self._session.commit()
