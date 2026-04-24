from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.product.category.cmd import (
    ChangeCategoryDescriptionDefaultLang,
    ChangeCategoryDescriptionDefaultLangCmd,
    ChangeCategoryNameDefaultLang,
    ChangeCategoryNameDefaultLangCmd,
    DeleteCategoryMedia,
    DeleteCategoryMediaCmd,
    RemoveCategoryDescription,
    RemoveCategoryDescriptionCmd,
    RemoveCategoryName,
    RemoveCategoryNameCmd,
    SetCategoryDescription,
    SetCategoryDescriptionCmd,
    SetCategoryMedia,
    SetCategoryMediaCmd,
    SetCategoryName,
    SetCategoryNameCmd,
    TranslateCategoryDescriptionToOthers,
    TranslateCategoryDescriptionToOthersCmd,
    TranslateCategoryNameToOthers,
    TranslateCategoryNameToOthersCmd,
)
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from presentation.aiogram.dialog.admin.category.edit.ctx import (
    CTX_KEY,
    CategoryEditingCtx,
)
from presentation.aiogram.mapper.file import FileDTOFactory
from presentation.aiogram.setting.category.model import CategorySettings


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[CategorySettings],
) -> None:
    ctx = CategoryEditingCtx(
        category_id=dialog_manager.start_data["category_id"],  # type: ignore[index, call-overload,arg-type]
        current_name_lang=settings.default_lang,
        current_description_lang=settings.default_lang,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_name(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    new_name: str,
    handler: FromDishka[SetCategoryName],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(
        SetCategoryNameCmd(
            id=ctx.category_id,
            lang=ctx.current_name_lang,
            name=new_name,
        ),
    )

    await event.delete()


@inject
async def on_edit_name_default_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[ChangeCategoryNameDefaultLang],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    return await handler(
        ChangeCategoryNameDefaultLangCmd(id=ctx.category_id, lang=lang),
    )


@inject
async def on_remove_name(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RemoveCategoryName],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    return await handler(
        RemoveCategoryNameCmd(id=ctx.category_id, lang=ctx.current_name_lang),
    )


@inject
async def on_translate_name_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[TranslateCategoryNameToOthers],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(
        TranslateCategoryNameToOthersCmd(
            id=ctx.category_id,
        ),
    )


@inject
async def on_select_name_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    ctx.current_name_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_description(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    new_description: str,
    handler: FromDishka[SetCategoryDescription],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(
        SetCategoryDescriptionCmd(
            id=ctx.category_id,
            lang=ctx.current_description_lang,
            description=new_description,
        ),
    )

    await event.delete()


@inject
async def on_edit_description_default_lang(
    event: CallbackQuery,
    select: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[ChangeCategoryDescriptionDefaultLang],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    return await handler(
        ChangeCategoryDescriptionDefaultLangCmd(id=ctx.category_id, lang=lang),
    )


@inject
async def on_translate_description_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[TranslateCategoryDescriptionToOthers],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(TranslateCategoryDescriptionToOthersCmd(id=ctx.category_id))


@inject
async def on_select_description_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    ctx.current_description_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_remove_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[RemoveCategoryDescription],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(
        cmd=RemoveCategoryDescriptionCmd(
            id=ctx.category_id,
            lang=ctx.current_description_lang,
        ),
    )


@inject
async def on_edit_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    handler: FromDishka[SetCategoryMedia],
    file_factory: FromDishka[FileDTOFactory],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(
        SetCategoryMediaCmd(
            id=ctx.category_id,
            media=await file_factory.from_message(msg=event),
        ),
    )

    await dialog_manager.done()


@inject
async def on_delete_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[DeleteCategoryMedia],
    retort: FromDishka[Retort],
) -> None:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    await handler(DeleteCategoryMediaCmd(id=ctx.category_id))
