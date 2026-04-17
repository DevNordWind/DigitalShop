import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession, Translator
from app.product.category.exception import CategoryNotFound
from app.user.service import GetCurrentUser
from domain.common.localized import Language
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.exception import (
    CategoryAccessDenied,
    CategoryDescriptionEmpty,
)
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryAccessService
from domain.product.category.value_object import CategoryId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class TranslateCategoryDescriptionToOthersCmd:
    id: UUID


class TranslateCategoryDescriptionToOthers:
    def __init__(
        self,
        repository: CategoryRepository,
        translator: Translator,
        current_user: GetCurrentUser,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._repository: CategoryRepository = repository
        self._translator: Translator = translator
        self._current_user: GetCurrentUser = current_user
        self._session: DatabaseSession = session
        self._clock: Clock = clock

    async def __call__(
        self,
        cmd: TranslateCategoryDescriptionToOthersCmd,
    ) -> None:
        editor: User = await self._current_user()

        if not CategoryAccessService.can_edit(editor=editor):
            raise CategoryAccessDenied

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFound

        if category.description is None:
            raise CategoryDescriptionEmpty

        source_text: str = category.description.get_default()

        coroutines: dict[Language, Awaitable[str]] = {}
        for lang in Language:
            if lang != category.description.default_lang:
                coroutines[lang] = self._translator.translate(
                    source=category.description.default_lang,
                    target=lang,
                    text=source_text,
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
