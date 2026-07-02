FixedItemNotFoundError =
    <b>❌ Товар не найден</b>

    <blockquote>ℹ️ Запрашиваемый фиксированный товар не найден.</blockquote>
    .call = ❌ Товар не найден

FixedItemContentReplacingForbiddenError =
    <b>❌ Замена содержимого запрещена</b>

    <blockquote>ℹ️ Иземенение заархивированного товара невозможно.</blockquote>
    .call = ❌ Иземенение заархивированного товара невозможно

FixedItemDeletionForbiddenError =
    <b>❌ Удаление запрещено</b>

    <blockquote>ℹ️ Товар сперва надо заархивировать.</blockquote>
    .call = ❌ Удаление запрещено

FixedItemArchivationForbiddenError = <b>❌ Архивация запрещена</b>
    .call = ❌ Архивация запрещена

FixedItemRecoverForbiddenError = <b>❌ Восстановление запрещено</b>
    .call = ❌ Восстановление запрещено

ItemContentTooLongError =
    <b>❌ Содержимое товара слишком длинное</b>

    <blockquote>ℹ️ Максимальная длина содержимого — { $max_length } символов.</blockquote>
    .call = ❌ Слишком товара длинное содержимое

ItemContentTooShortError =
    <b>❌ Содержимое товара слишком короткое</b>

    <blockquote>ℹ️ Минимальная длина содержимого — { $min_length } символов.</blockquote>
    .call = ❌ Слишком короткое содержимое

NegativeItemsAmountForbiddenError =
    <b>❌ Недопустимое количество</b>

    <blockquote>ℹ️ Количество товаров не может быть отрицательным.</blockquote>
    .call = ❌ Недопустимое количество

StockItemNotFoundError =
    <b>❌ Товар не найден</b>

    <blockquote>ℹ️ Запрашиваемый товар не найден.</blockquote>
    .call = ❌ Товар не найден

StockItemArchivationForbiddenError = { FixedItemArchivationForbiddenError }
    .call = { FixedItemArchivationForbiddenError.call }

StockItemContentReplacingForbiddenError = { FixedItemContentReplacingForbiddenError }
    .call = { FixedItemContentReplacingForbiddenError.call }

StockItemRecoverForbiddenError = { FixedItemRecoverForbiddenError }
    .call = { FixedItemRecoverForbiddenError.call }

StockItemReservationForbiddenError =
    <b>❌ Резервирование запрещено</b>

    <blockquote>ℹ️ На данном этапе резервирование невозможно</blockquote>
    .call = ❌ На данном этапе резервирование невозможно

StockItemSellForbiddenError =
    <b>❌ Продажа запрещена</b>

    <blockquote>ℹ️ На данном этапе продажа невозможна</blockquote>
    .call = ❌ На данном этапе продажа невозможна

StockItemReleaseForbiddenError =
    <b>❌ Освобождение резерва запрещено</b>

    <blockquote>ℹ️ Нельзя снять резерв со складского товара на данном этапе.</blockquote>
    .call = ❌ Освобождение запрещено

StockItemDeletionForbiddenError = { FixedItemDeletionForbiddenError }
    .call = { FixedItemDeletionForbiddenError.call }
