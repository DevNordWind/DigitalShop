admin-position-warehouse-stock = <b>{ -item-emoji } Товары</b>

    { -current } Тип хранилища: { warehouse-type }

    <blockquote>ℹ️ Нажми на товар, чтобы посмотреть информацию о нём</blockquote>
    .filters-btn = { -filter-emoji } Фильтры
    .btn = { $item_value } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }

admin-position-warehouse-stock-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order }{ -current }
    .status-btn = { $is_current ->
        [True] { -current } { item-status-plural } { -current }
        *[False] { item-status-plural }
    }

admin-position-warehouse-add-stock = <b>➕ Добавление товаров</b>

    { -current } <b>Товары</b> разделяются одной пустой строчкой, например:

    <code>Данные товара...</code>

    <code>Данные товара...</code>

    <code>Данные товара...</code>

    .success = <b>✅ Добавлено <code>{ $count }</code> { items-plural-lower-case }</b>

admin-position-warehouse-item-stock = <b>{ -item-emoji } Товар</b>

    <b>{ -current } Содержимое:</b> <code>{ $item_value }</code>
    { -time-emoji } Добавлен: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    { $item_status ->
        [SOLD]
            ├ Зарезервирован: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Продан: <i>{ DATETIME($sold_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [RESERVED] └ Зарезервирован: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [ARCHIVED] {""}
        <blockquote>🗄 Товар заархивирован <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        *[other] { unknown }
    }

admin-position-warehouse-archive-confirmation-stock = <b>🤔 Вы действительно хотите архивировать товар?</b>

    <blockquote>⚠️ Архивированный товар станет не доступен для покупки и изменений</blockquote>

admin-position-warehouse-delete-confirmation-stock = <b>🤔 Вы действительно хотите удалить товар?</b>

    <blockquote>⚠️ Удалённый товар будет <b>НЕВОЗМОЖНО</b> восстановить</blockquote>

admin-position-warehouse-archive-all-confirmation-stock = <b>🤔 Вы действительно хотите <b>ВСЕ</b> архивировать товары?</b>

    <blockquote>⚠️ Архивированные товары станут недоступны для покупки и редактирования</blockquote>

admin-position-warehouse-delete-all-confirmation-stock = <b>🤔 Вы действительно хотите удалить <b>ВСЕ</b> товары?</b>

    <blockquote>⚠️ Удалённые товары будет <b>НЕВОЗМОЖНО</b> восстановить. <i>Будут удалены только заархивированные товары</i></blockquote>
