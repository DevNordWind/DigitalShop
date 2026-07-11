from dataclasses import dataclass
from datetime import datetime

from app.domain.common.localized import Language
from app.domain.common.money import Currency, Money
from app.domain.shopping.category.value_object import (
    CategoryId,
)
from app.domain.shopping.position.const import MAX_MEDIA_LIMIT
from app.domain.shopping.position.enums import (
    FulfillmentType,
    PositionStatus,
    WarehouseType,
)
from app.domain.shopping.position.exception import (
    PositionArchivedError,
    PositionDeletionForbiddenError,
    PositionDescriptionEmptyError,
    PositionIncompatibleStrategyError,
    PositionMediaLimitReachedError,
    PositionMediaNotFoundError,
)
from app.domain.shopping.position.value_object import (
    PositionDescription,
    PositionId,
    PositionMediaKey,
    PositionName,
    PositionPrice,
    PositionSnapshot,
)
from app.domain.user.value_object import UserId


@dataclass
class Position:
    id: PositionId
    category_id: CategoryId
    creator_id: UserId

    name: PositionName
    description: PositionDescription | None
    media: list[PositionMediaKey]

    price: PositionPrice

    fulfillment_type: FulfillmentType
    warehouse_type: WarehouseType

    created_at: datetime
    updated_at: datetime | None

    archived_at: datetime | None

    status: PositionStatus = PositionStatus.AVAILABLE

    def __post_init__(self) -> None:
        if len(self.media) > MAX_MEDIA_LIMIT:
            raise PositionMediaLimitReachedError(limit=MAX_MEDIA_LIMIT)

        self._validate_strategies()

    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None and self.status == PositionStatus.ARCHIVED

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
        self.ensure_not_archived()

        self.name = self.name.set(lang=lang, translation=name)
        self.updated_at = now

    def change_name_default_lang(self, lang: Language, now: datetime) -> None:
        self.ensure_not_archived()

        if self.name.default_lang == lang:
            return

        self.name = self.name.change_default_lang(lang=lang)
        self.updated_at = now

    def remove_name(self, lang: Language, now: datetime) -> None:
        self.ensure_not_archived()

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
        self.ensure_not_archived()

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
        self.ensure_not_archived()

        if self.description is None:
            raise PositionDescriptionEmptyError

        if self.description.default_lang == lang:
            return

        self.description = self.description.change_default_lang(lang)
        self.updated_at = now

    def remove_description(self, lang: Language, now: datetime) -> None:
        self.ensure_not_archived()

        if self.description is None or not self.description.has(lang):
            return

        if self.description.default_lang == lang and len(self.description) == 1:
            self.description = None

        else:
            self.description = self.description.remove(lang)

        self.updated_at = now

    def add_media(self, media: PositionMediaKey, now: datetime) -> None:
        self.ensure_not_archived()

        if len(self.media) >= MAX_MEDIA_LIMIT:
            raise PositionMediaLimitReachedError(limit=MAX_MEDIA_LIMIT)

        self.media.append(media)
        self.updated_at = now

    def replace_media(
        self,
        old: PositionMediaKey,
        new: PositionMediaKey,
        now: datetime,
    ) -> None:
        self.ensure_not_archived()

        if old not in self.media:
            raise PositionMediaNotFoundError

        index = self.media.index(old)
        self.media[index] = new
        self.updated_at = now

    def remove_media(self, media: PositionMediaKey, now: datetime) -> None:
        self.ensure_not_archived()

        if media not in self.media:
            return

        self.media.remove(media)
        self.updated_at = now

    def set_price(self, price: Money, now: datetime) -> None:
        self.ensure_not_archived()

        self.price = self.price.set(price)
        self.updated_at = now

    def change_price_base_currency(
        self,
        currency: Currency,
        now: datetime,
    ) -> None:
        self.ensure_not_archived()

        self.price = self.price.change_base_currency(currency=currency)
        self.updated_at = now

    def take_snapshot(self) -> PositionSnapshot:
        return PositionSnapshot(
            category_id=self.category_id.value,
            position_id=self.id.value,
            price=self.price,
            position_name=self.name,
        )

    def ensure_deletable(self) -> None:
        if not self.is_archived:
            raise PositionDeletionForbiddenError

    def ensure_not_archived(self) -> None:
        if self.is_archived:
            raise PositionArchivedError

    def _validate_strategies(self) -> None:
        if (
            self.fulfillment_type == FulfillmentType.FIXED
            and self.warehouse_type == WarehouseType.FIXED
        ):
            return

        if (
            self.fulfillment_type == FulfillmentType.STOCK
            and self.warehouse_type == WarehouseType.UNLIMITED
        ):
            return

        raise PositionIncompatibleStrategyError
