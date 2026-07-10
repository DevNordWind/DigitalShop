admin-position-fixed-item =
    { $item_value }

    { -time-emoji } Додано: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>


admin-position-warehouse-fixed = <b>{ -item-emoji } Товари</b>

    { -current } Тип сховища: { warehouse-type }
    { -current } Товар: { $has_item ->
        [False] { unknown.emoji } не додано
        *[True] { $is_archived ->
            [False] { admin-position-fixed-item }
            *[True] { admin-position-fixed-item }

        <blockquote>🗄 Товар заархівовано <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        }
    }
    .replace-btn = 🔁 Замінити
    .warehouse-btn = 📦 Сховище
    .archive-btn = 🗄 Архів

admin-position-warehouse-archive-confirmation-fixed = <b>🤔 Ви дійсно хочете заархівувати товар?</b>

    <blockquote>⚠️ Заархівований товар стане недоступним для покупки та змін</blockquote>

admin-position-warehouse-delete-confirmation-fixed = <b>🤔 Ви дійсно хочете видалити товар?</b>

    <blockquote>⚠️ Видалений товар буде <b>НЕМОЖЛИВО</b> відновити</blockquote>

admin-position-warehouse-archive-fixed = <b>🗄 Архів</b>
    .btn = { $item_value } | { -date-emoji }{ DATETIME($archived_at, dateStyle: "short", timeStyle: "short")}

admin-position-warehouse-archived-item-fixed = <b>{ -item-emoji } Товар</b>

    <b>{ -current } Вміст:</b> <code>{ $item_value }</code>

    { -time-emoji } Додано: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    └ Заархівовано: <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i>

admin-position-warehouse-replace-fixed = <b>🔁 Заміна товару</b>

    <blockquote>ℹ️ Надішли вміст товару у вигляді тексту.</blockquote>

admin-position-warehouse-add-fixed = <b>➕ Додавання товару</b>

    <blockquote>ℹ️ Надішли вміст товару у вигляді тексту.</blockquote>
