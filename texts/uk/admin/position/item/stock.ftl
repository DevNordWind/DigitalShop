admin-position-warehouse-stock = <b>{ -item-emoji } Товари</b>

    { -current } Тип сховища: { warehouse-type }

    <blockquote>ℹ️ Натисни на товар, щоб переглянути інформацію про нього</blockquote>
    .filters-btn = { -filter-emoji } Фільтри
    .btn = { $item_value } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }

admin-position-warehouse-stock-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order }{ -current }
    .status-btn = { $is_current ->
        [True] { -current } { item-status-plural } { -current }
        *[False] { item-status-plural }
    }

admin-position-warehouse-add-stock = <b>➕ Додавання товарів</b>

    { -current } <b>Товари</b> розділяються одним порожнім рядком, наприклад:

    <code>Дані товару...</code>

    <code>Дані товару...</code>

    <code>Дані товару...</code>

    .success = <b>✅ Додано <code>{ $count }</code> { items-plural-lower-case }</b>

admin-position-warehouse-item-stock = <b>{ -item-emoji } Товар</b>

    <b>{ -current } Вміст:</b> <code>{ $item_value }</code>
    { -time-emoji } Додано: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    { $item_status ->
        [SOLD]
            ├ Зарезервовано: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Продано: <i>{ DATETIME($sold_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [RESERVED] └ Зарезервовано: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [ARCHIVED] {""}
        <blockquote>🗄 Товар заархівовано <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        *[other] { unknown }
    }

admin-position-warehouse-archive-confirmation-stock = <b>🤔 Ви дійсно хочете архівувати товар?</b>

    <blockquote>⚠️ Заархівований товар стане недоступним для покупки та змін</blockquote>

admin-position-warehouse-delete-confirmation-stock = <b>🤔 Ви дійсно хочете видалити товар?</b>

    <blockquote>⚠️ Видалений товар буде <b>НЕМОЖЛИВО</b> відновити</blockquote>

admin-position-warehouse-archive-all-confirmation-stock = <b>🤔 Ви дійсно хочете архівувати <b>ВСІ</b> товари?</b>

    <blockquote>⚠️ Заархівовані товари стануть недоступними для покупки та редагування</blockquote>

admin-position-warehouse-delete-all-confirmation-stock = <b>🤔 Ви дійсно хочете видалити <b>ВСІ</b> товари?</b>

    <blockquote>⚠️ Видалені товари буде <b>НЕМОЖЛИВО</b> відновити. <i>Будуть видалені лише заархівовані товари</i></blockquote>
