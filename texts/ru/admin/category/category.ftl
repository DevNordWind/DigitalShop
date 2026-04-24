admin-categories = <b>{ -category-emoji } Категории</b>
    .order-btn = { -current } { sorting-order } { -current }
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Настройки️
    .filters-btn = { -filter-emoji } Фильтры

admins-category-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admin-category = <b>{ -category-emoji } Редактирование категории</b>

    <b>📜 Основная информация:</b>
    { admin-category-name }
    { admin-category-description }
    { $updated_at ->
        [None] { -current } Дата создания: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Дата создания: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Последнее изменение: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Товары:</b>
    ├ Кол-во позиций: <code>{ $positions_amount }</code>
    { $is_archived ->
        [False] └ Кол-во товаров: <code>{ $items_amount }</code>
        *[True] └ Кол-во товаров: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Категория заархивирована <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
    }
    .show-language-btn = Показать на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Название
    .description-btn = Описание
    .media-btn = Медиа

admin-category-archive-confirmation = <b>🤔 Вы действительно хотите архивировать категорию <code>{ $name }</code>?</b>

    <blockquote>⚠️ <b>ВСЕ</b> позиции категории также будут заархивированы</blockquote>

admin-category-delete-confirmation = <b>🤔 Вы действительно хотите архивировать категорию { $name }</b>

    <blockquote>⚠️ Удалённую категорию будет <b>НЕВОЗМОЖНО</b> восстановить. <i><b>ВСЕ</b> позиции также будут удалены</i></blockquote>

admin-category-archive-all-confirmation = <b>🤔 Вы действительно хотите архивировать <i>ВСЕ</i> категории?</b>

    <blockquote>⚠️ Архивированные категории станут недоступны для покупки и редактирования.
    <b>ВСЕ</b> позиции категории также будут заархивированы</blockquote>

admin-category-delete-all-confirmation = <b>🤔 Вы действительно хотите удалить <i>ВСЕ</i> категории?</b>

    <blockquote>⚠️ Удалённые категории будет <b>НЕВОЗМОЖНО</b> восстановить.
    <i>Будут удалены только заархивированные позиции.
    <b>ВСЕ</b> позиции также будут удалены</i></blockquote>
