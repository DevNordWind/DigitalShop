import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession, Translator
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.localized import Language
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import (
    PositionDescriptionEmpty,
    PositionPermissionDenied,
)
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class TranslatePositionDescriptionToOthersCmd:
    id: UUID


class TranslatePositionDescriptionToOthers:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        translator: Translator,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._translator: Translator = translator
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(
        self,
        cmd: TranslatePositionDescriptionToOthersCmd,
    ) -> None:
        editor: User = await self._current_user()

        if not PositionAccessService.can_edit(editor_role=editor.role):
            raise PositionPermissionDenied

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        if position.description is None:
            raise PositionDescriptionEmpty

        source_text: str = position.description.get_default()

        coroutines: dict[Language, Awaitable[str]] = {}
        for lang in Language:
            if lang != position.description.default_lang:
                coroutines[lang] = self._translator.translate(
                    source=position.description.default_lang,
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
            position.set_description(
                lang=lang,
                description=description,
                now=now,
            )

        await self._session.commit()
