from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InputFile, Message

from domain.common.file import FileKey, FileType
from presentation.aiogram.mapper.file.mapper import FileKeyMapper


class FileSender:
    def __init__(self, mapper: FileKeyMapper, bot: Bot):
        self._mapper: FileKeyMapper = mapper
        self._bot: Bot = bot

    async def send(
        self,
        chat_id: int | str,
        key: FileKey,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | None:
        input_file: InputFile = await self._mapper.to_input_file(
            key=key,
            bot=self._bot,
        )

        match key.type:
            case FileType.DOCUMENT:
                return await self._bot.send_document(
                    chat_id=chat_id,
                    document=input_file,
                    reply_markup=reply_markup,
                )
            case FileType.PHOTO:
                return await self._bot.send_photo(
                    chat_id=chat_id,
                    photo=input_file,
                    reply_markup=reply_markup,
                )
            case FileType.GIF:
                return await self._bot.send_animation(
                    chat_id=chat_id,
                    animation=input_file,
                    reply_markup=reply_markup,
                )
            case FileType.VIDEO:
                return await self._bot.send_video(
                    chat_id=chat_id,
                    video=input_file,
                    reply_markup=reply_markup,
                )
