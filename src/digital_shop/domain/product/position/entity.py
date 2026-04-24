from dataclasses import dataclass
from datetime import datetime

from domain.common.localized import Language
from domain.common.money import Currency, Money
from domain.product.category.value_object import (
    CategoryId,
)
from domain.product.position.const import MAX_MEDIA_LIMIT
from domain.product.position.enums import PositionStatus
from domain.product.position.exception import (
    PositionArchived,
    PositionDeletionForbidden,
    PositionDescriptionEmpty,
    PositionMediaLimitReached,
    PositionMediaNotFound,
)
from domain.product.position.strategy import (
    WarehouseStrategy,
)
from domain.product.position.value_object import (
    PositionDescription,
    PositionId,
    PositionMediaKey,
    PositionName,
    PositionPrice,
)
from domain.user.value_object import UserId


@dataclass
class Position:
    id: PositionId
    category_id: CategoryId
    creator_id: UserId

    name: PositionName
    description: PositionDescription | None
    media: list[PositionMediaKey]
    warehouse: WarehouseStrategy

    price: PositionPrice

    created_at: datetime
    updated_at: datetime | None

    archived_at: datetime | None
    status: PositionStatus = PositionStatus.AVAILABLE

    def __post_init__(self) -> None:
        if len(self.media) > MAX_MEDIA_LIMIT:
            raise PositionMediaLimitReached(limit=MAX_MEDIA_LIMIT)

    @property
    def is_archived(self) -> bool:
        return (
            self.archived_at is not None
            and self.status == PositionStatus.ARCHIVED
        )

    def ensure_can_add_item(self, current: int, to_add: int) -> None:
        self._ensure_not_archived()
        self.warehouse.ensure_can_add(current, to_add)

    def ensure_can_acquire(self) -> None:
        self._ensure_not_archived()

    def archive(self, now: datetime) -> None:
        if self.is_archived:
            return

        self.status = PositionStatus.ARCHIVED
        self.archived_at = now
        self.updated_at = now

    def recover(self, now: datetime) -> None:
        if not self.is_archived:
            return

        self.status = PositionStatus.AVAILABLE
        self.archived_at = None
        self.updated_at = now

    def set_name(self, lang: Language, name: str, now: datetime) -> None:
        self._ensure_not_archived()

        self.name = self.name.set(lang=lang, translation=name)
        self.updated_at = now

    def change_name_default_lang(self, lang: Language, now: datetime) -> None:
        self._ensure_not_archived()

        if self.name.default_lang == lang:
            return

        self.name = self.name.change_default_lang(lang=lang)
        self.updated_at = now

    def remove_name(self, lang: Language, now: datetime) -> None:
        self._ensure_not_archived()

        if not self.name.has(lang):
            return

        self.name = self.name.remove(lang)
        self.updated_at = now

    def set_description(
        self,
        lang: Language,
        description: str,
        now: datetime,
    ) -> None:
        self._ensure_not_archived()

        if self.description is None:
            self.description = PositionDescription.create(
                lang=lang,
                translation=description,
            )
        else:
            self.description = self.description.set(
                lang=lang,
                translation=description,
            )

        self.updated_at = now

    def change_description_default_lang(
        self,
        lang: Language,
        now: datetime,
    ) -> None:
        self._ensure_not_archived()

        if self.description is None:
            raise PositionDescriptionEmpty

        if self.description.default_lang == lang:
            return

        self.description = self.description.change_default_lang(lang)
        self.updated_at = now

    def remove_description(self, lang: Language, now: datetime) -> None:
        self._ensure_not_archived()

        if self.description is None or not self.description.has(lang):
            return

        if (
            self.description.default_lang == lang
            and len(self.description) == 1
        ):
            self.description = None

        else:
            self.description = self.description.remove(lang)

        self.updated_at = now

    def add_media(self, media: PositionMediaKey, now: datetime) -> None:
        self._ensure_not_archived()

        if len(self.media) >= MAX_MEDIA_LIMIT:
            raise PositionMediaLimitReached(limit=MAX_MEDIA_LIMIT)

        self.media.append(media)
        self.updated_at = now

    def replace_media(
        self,
        old: PositionMediaKey,
        new: PositionMediaKey,
        now: datetime,
    ) -> None:
        self._ensure_not_archived()

        if old not in self.media:
            raise PositionMediaNotFound(old)

        index = self.media.index(old)
        self.media[index] = new
        self.updated_at = now

    def remove_media(self, media: PositionMediaKey, now: datetime) -> None:
        self._ensure_not_archived()

        if media not in self.media:
            return

        self.media.remove(media)
        self.updated_at = now

    def set_price(self, price: Money, now: datetime) -> None:
        self._ensure_not_archived()

        self.price = self.price.set(price)
        self.updated_at = now

    def change_price_base_currency(
        self,
        currency: Currency,
        now: datetime,
    ) -> None:
        self._ensure_not_archived()

        self.price = self.price.change_base_currency(currency=currency)
        self.updated_at = now

    def ensure_deletable(self) -> None:
        if not self.is_archived:
            raise PositionDeletionForbidden

    def _ensure_not_archived(self) -> None:
        if self.is_archived:
            raise PositionArchived
