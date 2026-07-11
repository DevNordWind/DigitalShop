FixedItemNotFoundError =
    <b>❌ Товар не знайдено</b>

    <blockquote>ℹ️ Запитуваний фіксований товар не знайдено.</blockquote>
    .call = ❌ Товар не знайдено

FixedItemContentReplacingForbiddenError =
    <b>❌ Заміну вмісту заборонено</b>

    <blockquote>ℹ️ Зміна заархівованого товару неможлива.</blockquote>
    .call = ❌ Зміна заархівованого товару неможлива

FixedItemDeletionForbiddenError =
    <b>❌ Видалення заборонено</b>

    <blockquote>ℹ️ Товар спочатку потрібно заархівувати.</blockquote>
    .call = ❌ Видалення заборонено

FixedItemArchivationForbiddenError = <b>❌ Архівування заборонено</b>
    .call = ❌ Архівування заборонено

FixedItemRecoverForbiddenError = <b>❌ Відновлення заборонено</b>
    .call = ❌ Відновлення заборонено

ItemContentTooLongError =
    <b>❌ Вміст товару занадто довгий</b>

    <blockquote>ℹ️ Максимальна довжина вмісту — { $max_length } символів.</blockquote>
    .call = ❌ Вміст товару занадто довгий

ItemContentTooShortError =
    <b>❌ Вміст товару занадто короткий</b>

    <blockquote>ℹ️ Мінімальна довжина вмісту — { $min_length } символів.</blockquote>
    .call = ❌ Занадто короткий вміст

NegativeItemsAmountForbiddenError =
    <b>❌ Неприпустима кількість</b>

    <blockquote>ℹ️ Кількість товарів не може бути від'ємною.</blockquote>
    .call = ❌ Неприпустима кількість

StockItemNotFoundError =
    <b>❌ Товар не знайдено</b>

    <blockquote>ℹ️ Запитуваний товар не знайдено.</blockquote>
    .call = ❌ Товар не знайдено

StockItemArchivationForbiddenError = { FixedItemArchivationForbiddenError }
    .call = { FixedItemArchivationForbiddenError.call }

StockItemContentReplacingForbiddenError = { FixedItemContentReplacingForbiddenError }
    .call = { FixedItemContentReplacingForbiddenError.call }

StockItemRecoverForbiddenError = { FixedItemRecoverForbiddenError }
    .call = { FixedItemRecoverForbiddenError.call }

StockItemReservationForbiddenError =
    <b>❌ Резервування заборонено</b>

    <blockquote>ℹ️ На цьому етапі резервування неможливе</blockquote>
    .call = ❌ На цьому етапі резервування неможливе

StockItemSellForbiddenError =
    <b>❌ Продаж заборонено</b>

    <blockquote>ℹ️ На цьому етапі продаж неможливий</blockquote>
    .call = ❌ На цьому етапі продаж неможливий

StockItemReleaseForbiddenError =
    <b>❌ Зняття резерву заборонено</b>

    <blockquote>ℹ️ Неможливо зняти резерв зі складського товару на цьому етапі.</blockquote>
    .call = ❌ Зняття резерву заборонено

StockItemDeletionForbiddenError = { FixedItemDeletionForbiddenError }
    .call = { FixedItemDeletionForbiddenError.call }
