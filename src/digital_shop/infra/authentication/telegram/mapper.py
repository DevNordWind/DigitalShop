from domain.user.enums import UserRole
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.authentication.telegram.model import TelegramContext


class TelegramContextMapper:
    @classmethod
    def to_dto(
        cls, src: TelegramContext, role: UserRole
    ) -> TelegramContextDTO:
        return TelegramContextDTO(
            id=src.id,
            user_id=src.user_id.value,
            user_role=role,
            tg_username=src.tg_username,
            tg_first_name=src.tg_first_name,
            lang=src.lang,
            is_active=src.is_active,
            currency=src.currency,
        )
