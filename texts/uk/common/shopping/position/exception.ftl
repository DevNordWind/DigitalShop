PositionPermissionDeniedError =
    <b>❌ Недостатньо прав</b>

    <blockquote>ℹ️ У вас немає прав для виконання цієї дії з позицією.</blockquote>
    .call = ❌ Недостатньо прав

PositionMediaNotFoundError =
    <b>❌ Медіафайл не знайдено</b>

    <blockquote>ℹ️ Запитуваний медіафайл позиції не знайдено.</blockquote>
    .call = ❌ Медіафайл не знайдено

PositionNotFoundError =
    <b>❌ Позицію не знайдено</b>

    <blockquote>ℹ️ Запитувана позиція не існує або була видалена.</blockquote>
    .call = ❌ Позицію не знайдено

PositionAlreadyArchivedError =
    <b>❌ Позиція вже заархівована</b>

    <blockquote>ℹ️ Позиція вже знаходиться в архіві.</blockquote>
    .call = ❌ Вже заархівована

PositionNotArchivedError =
    <b>❌ Позиція не заархівована</b>

    <blockquote>ℹ️ Ця дія доступна тільки для заархівованих позицій.</blockquote>
    .call = ❌ Не заархівована

PositionDescriptionEmptyError =
    <b>❌ Опис відсутній</b>

    <blockquote>ℹ️ Опис позиції не заповнено.</blockquote>
    .call = ❌ Опис відсутній

PositionNameAlreadyTakenError =
    <b>❌ Назва вже зайнята</b>

    <blockquote>ℹ️ Назва позиції для мови <b>{ $lang }</b> вже використовується.</blockquote>
    .call = ❌ Назва зайнята

PositionMediaLimitReachedError =
    <b>❌ Досягнуто ліміт медіафайлів</b>

    <blockquote>ℹ️ Максимальна кількість медіафайлів: { $limit }.</blockquote>
    .call = ❌ Ліміт медіафайлів

PositionChangingForbiddenError =
    <b>❌ Зміна заборонена</b>

    <blockquote>ℹ️ Зміна цієї позиції заборонена.</blockquote>
    .call = ❌ Зміна заборонена

PositionArchivedError =
    <b>❌ Позиція заархівована</b>

    <blockquote>ℹ️ Дія неможлива, оскільки позиція знаходиться в архіві.</blockquote>
    .call = ❌ Позиція заархівована

PositionDeletionForbiddenError =
    <b>❌ Видалення заборонено</b>

    <blockquote>ℹ️ Видаляти можна лише заархівовані позиції.</blockquote>
    .call = ❌ Видаляти можна лише заархівовані позиції.

PositionWarehouseFullError =
    <b>❌ Склад переповнений</b>

    <blockquote>ℹ️ Неможливо додати товар, оскільки склад переповнений.</blockquote>
    .call = ❌ Склад переповнений

PositionItemNotFoundError =
    <b>❌ Товар не знайдено</b>

    <blockquote>ℹ️ Запитуваний товар позиції не знайдено.</blockquote>
    .call = ❌ Товар не знайдено

PositionDescriptionTooShortError =
    <b>❌ Опис занадто короткий</b>

    <blockquote>ℹ️ Мінімальна довжина опису — { $min_length } символів.</blockquote>
    .call = ❌ Опис занадто короткий

PositionDescriptionTooLongError =
    <b>❌ Опис занадто довгий</b>

    <blockquote>ℹ️ Максимальна довжина опису — { $max_length } символів.</blockquote>
    .call = ❌ Опис занадто довгий

PositionNameTooShortError =
    <b>❌ Назва занадто коротка</b>

    <blockquote>ℹ️ Мінімальна довжина назви — { $min_length } символів.</blockquote>
    .call = ❌ Назва занадто коротка

PositionNameTooLongError =
    <b>❌ Назва занадто довга</b>

    <blockquote>ℹ️ Максимальна довжина назви — { $max_length } символів.</blockquote>
    .call = ❌ Назва занадто довга

CurrencyMissingError =
    <b>❌ Ціну в одній із валют не вказано</b>

    <blockquote>ℹ️ Для валюти <b>{ currency }</b> не задано ціну.</blockquote>
    .call = ❌ Ціну для { currency } не вказано

OutOfStockError =
    <b>❌ Недостатньо товару</b>

    <blockquote>ℹ️ Доступно лише { $available } шт.</blockquote>
    .call = ❌ Недостатньо товару
