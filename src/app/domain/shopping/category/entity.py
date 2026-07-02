from dataclasses import dataclass
from datetime import datetime

from app.domain.common.localized import Language
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.exception import (
    CategoryAlreadyArchivedError,
    CategoryAlreadyRecoveredError,
    CategoryArchivedError,
    CategoryDeletionForbiddenError,
    CategoryDescriptionEmptyError,
)
from app.domain.shopping.category.value_object import (
    CategoryDescription,
    CategoryId,
    CategoryMediaKey,
    CategoryName,
)
from app.domain.user.value_object import UserId


@dataclass
class Category:
    id: CategoryId
    creator_id: UserId

    name: CategoryName
    description: CategoryDescription | None
    media: CategoryMediaKey | None

    created_at: datetime
    updated_at: datetime | None

    archived_at: datetime | None
    status: CategoryStatus = CategoryStatus.AVAILABLE

    def ensure_can_add_positions(self) -> None:
        if self.status == CategoryStatus.ARCHIVED:
            raise CategoryArchivedError

    def archive(self, now: datetime) -> None:
        if self.status == CategoryStatus.ARCHIVED:
            raise CategoryAlreadyArchivedError

        self.status = CategoryStatus.ARCHIVED
        self.archived_at = now
        self.updated_at = now

    def recover(self, now: datetime) -> None:
        if self.status != CategoryStatus.ARCHIVED:
            raise CategoryAlreadyRecoveredError

        self.status = CategoryStatus.AVAILABLE
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
            self.description = CategoryDescription.create(
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
            raise CategoryDescriptionEmptyError

        if self.description.default_lang == lang:
            return

        self.description = self.description.change_default_lang(lang)
        self.updated_at = now

    def remove_description(self, lang: Language, now: datetime) -> None:
        self._ensure_not_archived()

        if self.description is None or not self.description.has(lang):
            return

        if self.description.default_lang == lang and len(self.description) == 1:
            self.description = None
        else:
            self.description = self.description.remove(lang)

        self.updated_at = now

    def set_media(self, media: CategoryMediaKey, now: datetime) -> None:
        self._ensure_not_archived()

        self.media = media
        self.updated_at = now

    def delete_media(self, now: datetime) -> None:
        self._ensure_not_archived()

        if self.media is None:
            return

        self.media = None
        self.updated_at = now

    def ensure_deletable(self) -> None:
        if self.status != CategoryStatus.ARCHIVED:
            raise CategoryDeletionForbiddenError

    def _ensure_not_archived(self) -> None:
        if self.status == CategoryStatus.ARCHIVED:
            raise CategoryArchivedError
