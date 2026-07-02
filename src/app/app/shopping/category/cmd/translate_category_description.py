import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.common.port.translator import Translator
from app.domain.common.localized import Language
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import (
    CategoryDescriptionEmptyError,
    CategoryNotFoundError,
)
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId


@dataclass(slots=True, frozen=True)
class TranslateCategoryDescriptionToOthersCmd:
    id: UUID


class TranslateCategoryDescriptionToOthers:
    def __init__(
        self,
        repository: CategoryRepository,
        translator: Translator,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._repository = repository
        self._translator = translator
        self._actor_provider = actor_provider
        self._session = session
        self._clock = clock

    async def __call__(
        self,
        cmd: TranslateCategoryDescriptionToOthersCmd,
    ) -> None:
        CategoryAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        if category.description is None:
            raise CategoryDescriptionEmptyError

        coroutines: dict[Language, Awaitable[str]] = {}
        for lang in Language:
            if lang != category.description.default_lang:
                coroutines[lang] = self._translator.translate(
                    source=category.description.default_lang,
                    target=lang,
                    text=category.description.default,
                )

        results: list[str] = await asyncio.gather(
            *(tuple(coroutines.values())),
        )

        translations: dict[Language, str] = dict(
            zip(coroutines.keys(), results, strict=True),
        )

        now: datetime = self._clock.now()

        for lang, description in translations.items():
            category.set_description(
                lang=lang,
                description=description,
                now=now,
            )

        await self._session.commit()
