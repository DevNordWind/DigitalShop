admin-position-fixed-item =
    { $item_value }

    { -time-emoji } Добавлен: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>


admin-position-warehouse-fixed = <b>{ -item-emoji } Товары</b>

    { -current } Тип хранилища: { warehouse-type }
    { -current } Товар: { $has_item ->
        [False] { unknown.emoji } не добавлен
        *[True] { $is_archived ->
            [False] { admin-position-fixed-item }
            *[True] { admin-position-fixed-item }

        <blockquote>🗄 Товар заархивирован <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        }
    }
    .replace-btn = 🔁 Заменить
    .warehouse-btn = 📦 Хранилище
    .archive-btn = 🗄 Архив

admin-position-warehouse-archive-confirmation-fixed = <b>🤔 Вы действительно хотите архивировать товар?</b>

    <blockquote>⚠️ Архивированный товар станет не доступен для покупки и изменений</blockquote>

admin-position-warehouse-delete-confirmation-fixed = <b>🤔 Вы действительно хотите удалить товар?</b>

    <blockquote>⚠️ Удалённый товар будет <b>НЕВОЗМОЖНО</b> восстановить</blockquote>

admin-position-warehouse-archive-fixed = <b>🗄 Архив</b>
    .btn = { $item_value } | { -date-emoji }{ DATETIME($archived_at, dateStyle: "short", timeStyle: "short")}

admin-position-warehouse-archived-item-fixed = <b>{ -item-emoji } Товар</b>

    <b>{ -current } Содержимое:</b> <code>{ $item_value }</code>

    { -time-emoji } Добавлен: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    └ Заархивирован: <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i>

admin-position-warehouse-replace-fixed = <b>🔁 Замена товара</b>

    <blockquote>ℹ️ Пришли содержимое товара в виде текста.</blockquote>

admin-position-warehouse-add-fixed = <b>➕ Добавление товара</b>

    <blockquote>ℹ️ Пришли содержимое товара в виде текста.</blockquote>
