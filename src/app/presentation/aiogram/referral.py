from aiogram import Bot
from aiogram.types import Message, TelegramObject
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload


async def create_ref_deeplink(bot: Bot, tg_user_id: int) -> str:
    return await create_start_link(bot, f"ref:{tg_user_id}", encode=True)


def extract_ref_deeplink(event: TelegramObject) -> int | None:
    if not isinstance(event, Message):
        return None

    if not event.text:
        return None

    parts = event.text.split(maxsplit=1)
    if len(parts) < 2:  # noqa: PLR2004
        return None

    payload_encoded = parts[1]
    try:
        payload = decode_payload(payload_encoded)
    except Exception:
        return None

    if not payload.startswith("ref:"):
        return None
    _, user_id_str = payload.split(":", 1)

    return int(user_id_str)
