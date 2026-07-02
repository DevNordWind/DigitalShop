PositionPermissionDeniedError =
    <b>❌ Недостаточно прав</b>

    <blockquote>ℹ️ У вас нет прав для выполнения этого действия с позицией.</blockquote>
    .call = ❌ Недостаточно прав

PositionMediaNotFoundError =
    <b>❌ Медиафайл не найден</b>

    <blockquote>ℹ️ Запрашиваемый медиафайл позиции не найден.</blockquote>
    .call = ❌ Медиафайл не найден

PositionNotFoundError =
    <b>❌ Позиция не найдена</b>

    <blockquote>ℹ️ Запрашиваемая позиция не существует или была удалена.</blockquote>
    .call = ❌ Позиция не найдена

PositionAlreadyArchivedError =
    <b>❌ Позиция уже заархивирована</b>

    <blockquote>ℹ️ Позиция уже находится в архиве.</blockquote>
    .call = ❌ Уже архивирована

PositionNotArchivedError =
    <b>❌ Позиция не архивирована</b>

    <blockquote>ℹ️ Это действие доступно только для архивированных позиций.</blockquote>
    .call = ❌ Не архивирована

PositionDescriptionEmptyError =
    <b>❌ Описание отсутствует</b>

    <blockquote>ℹ️ Описание позиции не заполнено.</blockquote>
    .call = ❌ Описание отсутствует

PositionNameAlreadyTakenError =
    <b>❌ Название уже занято</b>

    <blockquote>ℹ️ Название позиции для языка <b>{ $lang }</b> уже используется.</blockquote>
    .call = ❌ Название занято

PositionMediaLimitReachedError =
    <b>❌ Достигнут лимит медиафайлов</b>

    <blockquote>ℹ️ Максимальное количество медиафайлов: { $limit }.</blockquote>
    .call = ❌ Лимит медиафайлов

PositionChangingForbiddenError =
    <b>❌ Изменение запрещено</b>

    <blockquote>ℹ️ Изменение данной позиции запрещено.</blockquote>
    .call = ❌ Изменение запрещено

PositionArchivedError =
    <b>❌ Позиция заархивирована</b>

    <blockquote>ℹ️ Действие невозможно, так как позиция находится в архиве.</blockquote>
    .call = ❌ Позиция архивирована

PositionDeletionForbiddenError =
    <b>❌ Удаление запрещено</b>

    <blockquote>ℹ️ Только заархивированный позиции можно удалять.</blockquote>
    .call = ❌ Только заархивированный позиции можно удалять.

PositionWarehouseFullError =
    <b>❌ Склад переполнен</b>

    <blockquote>ℹ️ Невозможно добавить товар, так как склад переполнен.</blockquote>
    .call = ❌ Склад переполнен

OutOfStockError =
    <b>❌ Недостаточно товара</b>

    <blockquote>ℹ️ Доступно только { $available } шт.</blockquote>
    .call = ❌ Недостаточно товара

PositionItemNotFoundError =
    <b>❌ Товар не найден</b>

    <blockquote>ℹ️ Запрашиваемый товар позиции не найден.</blockquote>
    .call = ❌ Товар не найден

PositionDescriptionTooShortError =
    <b>❌ Описание слишком короткое</b>

    <blockquote>ℹ️ Минимальная длина описания — { $min_length } символов.</blockquote>
    .call = ❌ Описание слишком короткое

PositionDescriptionTooLongError =
    <b>❌ Описание слишком длинное</b>

    <blockquote>ℹ️ Максимальная длина описания — { $max_length } символов.</blockquote>
    .call = ❌ Описание слишком длинное

PositionNameTooShortError =
    <b>❌ Название слишком короткое</b>

    <blockquote>ℹ️ Минимальная длина названия — { $min_length } символов.</blockquote>
    .call = ❌ Название слишком короткое

PositionNameTooLongError =
    <b>❌ Название слишком длинное</b>

    <blockquote>ℹ️ Максимальная длина названия — { $max_length } символов.</blockquote>
    .call = ❌ Название слишком длинное

CurrencyMissingError =
    <b>❌ Цена в одной из валют не указана</b>

    <blockquote>ℹ️ Для валюты <b>{ currency }</b> не задана цена.</blockquote>
    .call = ❌ Цена для { currency } не указана
