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
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import (
    PositionNotFoundError,
)
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class TranslatePositionNameToOthersCmd:
    id: UUID


class TranslatePositionNameToOthers:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        translator: Translator,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._translator = translator
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(
        self,
        cmd: TranslatePositionNameToOthersCmd,
    ) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())
        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        coroutines: dict[Language, Awaitable[str]] = {}
        for lang in Language:
            if lang != position.name.default_lang:
                coroutines[lang] = self._translator.translate(
                    source=position.name.default_lang,
                    target=lang,
                    text=position.name.default,
                )

        results: list[str] = await asyncio.gather(
            *(tuple(coroutines.values())),
        )

        translations: dict[Language, str] = dict(
            zip(coroutines.keys(), results, strict=True),
        )

        now: datetime = self._clock.now()

        for lang, name in translations.items():
            position.set_name(lang=lang, name=name, now=now)

        await self._session.commit()
