from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.app.common.dto.localized import LocalizedTextDTO
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import File, FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.app.shopping.position.dto.description.mapper import PositionDescriptionMapper
from app.app.shopping.position.dto.name import PositionNameMapper
from app.app.shopping.position.dto.price import PositionPriceDTO, PositionPriceMapper
from app.domain.common.actor import UserActor
from app.domain.common.file_key import FileKeyRaw
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import FulfillmentType, WarehouseType
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionDomainService,
)
from app.domain.shopping.position.value_object import (
    PositionDescription,
    PositionId,
)


@dataclass(slots=True, frozen=True)
class CreatePositionCmd:
    category_id: UUID
    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: list[FileKeyRawDTO]
    price: PositionPriceDTO

    warehouse_type: WarehouseType
    fulfillment_type: FulfillmentType


class CreatePosition:
    def __init__(
        self,
        position_repo: PositionRepository,
        category_repo: CategoryRepository,
        service: PositionDomainService,
        session: DatabaseSession,
        file_session: FileStorageSession,
        actor_provider: ActorProvider,
    ):
        self._position_repo = position_repo
        self._category_repo = category_repo
        self._service = service
        self._session = session
        self._file_session = file_session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: CreatePositionCmd) -> PositionId:
        actor: UserActor = PositionAccessService.ensure_can_create(
            actor=await self._actor_provider.get()
        )

        category: Category | None = await self._category_repo.get(
            category_id=CategoryId(cmd.category_id),
        )
        if not category:
            raise CategoryNotFoundError

        name = PositionNameMapper.to_value_object(src=cmd.name)
        media_raw: list[FileKeyRaw] = [
            FileKeyRawMapper.to_value_object(src=key) for key in cmd.media
        ]
        price = PositionPriceMapper.to_value_object(src=cmd.price)
        description: PositionDescription | None = None

        if cmd.description:
            description = PositionDescriptionMapper.to_value_object(
                src=cmd.description,
            )

        position: Position = self._service.create(
            category=category,
            name=name,
            creator_id=actor.id,
            description=description,
            media_raw=media_raw,
            warehouse_type=cmd.warehouse_type,
            price=price,
            fulfillment_type=cmd.fulfillment_type,
        )

        position_id: PositionId = position.id

        if position.media:
            files = [
                File(key=media, content=raw.content)
                for media, raw in zip(position.media, cmd.media, strict=True)
            ]
            await self._file_session.put_many(files)
            await self._file_session.commit()

        await self._position_repo.add(position)
        await self._session.commit()

        return position_id
