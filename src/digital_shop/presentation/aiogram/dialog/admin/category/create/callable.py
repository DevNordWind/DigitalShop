import asyncio
from collections.abc import Awaitable
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import (
    MessageInput,
    TextInput,
)
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.file_key import FileKeyRawDTO
from app.common.dto.localized import LocalizedTextDTO
from app.common.port import Translator
from app.product.category.cmd import CreateCategory, CreateCategoryCmd
from app.product.category.dto.description import CategoryDescriptionMapper
from app.product.category.dto.name import CategoryNameMapper
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from presentation.aiogram.dialog.admin.category.create.ctx import (
    CTX_KEY,
    CategoryCreationContext,
)
from presentation.aiogram.mapper.file import FileDTOFactory
from presentation.aiogram.mapper.media_attachment import (
    MediaAttachmentFactory,
)
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.state import CreateCategoryState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[CategorySettings],
) -> None:

    localized_text = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations={},
    )
    ctx = CategoryCreationContext(
        name=localized_text,
        description=localized_text,
        media=None,
        show_lang=settings.default_lang,
        name_current_lang=settings.default_lang,
        description_current_lang=settings.default_lang,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_language(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.show_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_name(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    name: str,
    retort: FromDishka[Retort],
) -> None | Message:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.name.translations[ctx.name_current_lang] = name

    CategoryNameMapper.to_value_object(src=ctx.name)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return None


@inject
async def on_select_name_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.name_current_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_description(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    description: str,
    retort: FromDishka[Retort],
) -> None | Message:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.description.translations[ctx.description_current_lang] = description

    CategoryDescriptionMapper.to_value_object(src=ctx.description)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return None


@inject
async def on_clear_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.description.translations.pop(ctx.description_current_lang)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_description_lang(
    event: CallbackQuery,
    select: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.description_current_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryCreationContext = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.media = MediaAttachmentFactory.from_message(msg=event)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await event.delete()
    return await dialog_manager.switch_to(
        state=CreateCategoryState.view,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_clear_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )
    ctx.media = None
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_confirm(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[CreateCategory],
    file_factory: FromDishka[FileDTOFactory],
) -> None | bool:
    ctx: CategoryCreationContext = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    category_media: FileKeyRawDTO | None = (
        await file_factory.from_media_attachment(attachment=ctx.media)
        if ctx.media
        else None
    )

    await handler(
        cmd=CreateCategoryCmd(
            name=ctx.name,
            description=ctx.description
            if ctx.description.translations
            else None,
            media=category_media,
        ),
    )

    await dialog_manager.done()

    return None


@inject
async def on_translate_name_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    translator: FromDishka[Translator],
    retort: FromDishka[Retort],
    settings: FromDishka[CategorySettings],
) -> None:
    ctx: CategoryCreationContext = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    source_text: str = ctx.name.translations[settings.default_lang]

    coroutines: dict[Language, Awaitable[str]] = {}
    for lang in Language:
        if lang != settings.default_lang:
            coroutines[lang] = translator.translate(
                source=settings.default_lang,
                target=lang,
                text=source_text,
            )

    results: list[str] = await asyncio.gather(*(tuple(coroutines.values())))

    translations: dict[Language, str] = dict(
        zip(coroutines.keys(), results, strict=True),
    )

    ctx.name = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations=dict(translations.items())
        | {settings.default_lang: source_text},
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_translate_description_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    translator: FromDishka[Translator],
    retort: FromDishka[Retort],
    settings: FromDishka[CategorySettings],
) -> None:
    ctx: CategoryCreationContext = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    source_text: str = ctx.description.translations[settings.default_lang]

    coroutines: dict[Language, Awaitable[str]] = {}
    for lang in Language:
        if lang != settings.default_lang:
            coroutines[lang] = translator.translate(
                source=settings.default_lang,
                target=lang,
                text=source_text,
            )

    results: list[str] = await asyncio.gather(*(tuple(coroutines.values())))

    translations: dict[Language, str] = dict(
        zip(coroutines.keys(), results, strict=True),
    )

    ctx.description = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations=dict(translations.items())
        | {settings.default_lang: source_text},
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
