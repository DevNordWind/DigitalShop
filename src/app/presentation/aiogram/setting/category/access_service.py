from app.domain.user.enums import UserRole
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.category.exception import (
    CategorySettingsPermissionDeniedError,
)


class CategorySettingsAccessService:
    @classmethod
    def ensure_can_edit(cls, ctx: TelegramContextDTO) -> None:
        if ctx.user_role >= UserRole.ADMIN:
            return

        raise CategorySettingsPermissionDeniedError
