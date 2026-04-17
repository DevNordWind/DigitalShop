from dataclasses import dataclass
from uuid import UUID

from app.common.dto.file_key import (
    FileKeyRawDTO,
    FileKeyRawMapper,
)
from app.common.dto.localized import LocalizedTextDTO
from app.common.port import DatabaseSession
from app.common.port.file_storage import FileStorageSession
from app.product.category.exception import CategoryNotFound
from app.product.position.dto.description.mapper import (
    PositionDescriptionMapper,
)
from app.product.position.dto.name import PositionNameMapper
from app.product.position.dto.price import (
    PositionPriceDTO,
    PositionPriceMapper,
)
from app.user.service import GetCurrentUser
from domain.common.file import FileKeyRaw
from domain.product.category.entity import Category
from domain.product.category.port import CategoryRepository
from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.enums.warehouse import WarehouseType
from domain.product.position.port import PositionRepository
from domain.product.position.service import (
    PositionService,
    PositionWarehouseService,
)
from domain.product.position.value_object import (
    PositionDescription,
    PositionId,
    PositionMediaKey,
)
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class CreatePositionCmd:
    category_id: UUID
    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: list[FileKeyRawDTO]
    price: PositionPriceDTO
    warehouse_type: WarehouseType


class CreatePosition:
    def __init__(
        self,
        position_repo: PositionRepository,
        category_repo: CategoryRepository,
        service: PositionService,
        warehouse_service: PositionWarehouseService,
        session: DatabaseSession,
        file_session: FileStorageSession,
        current_user: GetCurrentUser,
    ):
        self._position_repo: PositionRepository = position_repo
        self._category_repo: CategoryRepository = category_repo
        self._service: PositionService = service
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._session: DatabaseSession = session
        self._file_session: FileStorageSession = file_session
        self._current_user: GetCurrentUser = current_user

    async def __call__(self, cmd: CreatePositionCmd) -> PositionId:
        creator: User = await self._current_user()

        category: Category | None = await self._category_repo.get(
            category_id=CategoryId(cmd.category_id),
        )
        if not category:
            raise CategoryNotFound

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
            creator=creator,
            name=name,
            description=description,
            media_raw=media_raw,
            warehouse_type=cmd.warehouse_type,
            price=price,
        )

        position_id: PositionId = position.id

        position_media: list[PositionMediaKey] = position.media

        if position.media:
            keys = [
                (key, raw.content)
                for key, raw in zip(position_media, cmd.media, strict=True)
            ]
            await self._file_session.put_many(keys)
            await self._file_session.commit()

        await self._position_repo.add(position)
        await self._session.commit()

        return position_id
