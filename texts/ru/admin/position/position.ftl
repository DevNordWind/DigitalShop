admin-positions-categories = <b>{ -category-emoji } Выбери категорию</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Настройки️
    .filters-btn = { -filter-emoji } Фильтры

admin-positions-category-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admins-position-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { position-status-plural } { -current }
        *[other] { position-status-plural }
    }

admin-positions = <b>{ -position-emoji } Позиции</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Настройки️
    .filters-btn = { -filter-emoji } Фильтры

admin-position = <b>{ -position-emoji } Редактирование позиции</b>

    <b>📜 Основная информация:</b>
    { admin-position-name }
    { admin-position-description }
    { $updated_at ->
        [None] { -current } Дата создания: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Дата создания: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Последнее изменение: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Цены:</b>
    { $prices }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Товары:</b>
    { $is_archived ->
        [False] └ Кол-во товаров: <code>{ $items_amount }</code>
        *[True] └ Кол-во товаров: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Позиция заархивирована</blockquote>
    }
    .show-language-btn = Показать на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Название
    .description-btn = Описание
    .media-btn = Медиа
    .price-btn = Цены
    .items-btn = Товары

admin-position-archive-confirmation = <b>🤔 Вы действительно хотите архивировать позицию <code>{ $name }</code>?</b>

    <blockquote>⚠️ Архивированная позиция станет недоступной для покупки и редактирования</blockquote>

admin-position-delete-confirmation = <b>🤔 Вы действительно хотите удалить позицию <code>{ $name }</code>?</b>

    <blockquote>⚠️ Удалённую позицию будет <b>НЕВОЗМОЖНО</b> восстановить</blockquote>

admin-position-archive-all-confirmation = <b>🤔 Вы действительно хотите архивировать <i>ВСЕ</i> позиции?</b>

    <blockquote>⚠️ Архивированные позиции станут недоступны для покупки и редактирования</blockquote>

admin-position-delete-all-confirmation = <b>🤔 Вы действительно хотите удалить <i>ВСЕ</i> позиции?</b>

    <blockquote>⚠️ Удалённые позиции будет <b>НЕВОЗМОЖНО</b> восстановить. <i>Будут удалены только заархивированные позиции</i></blockquote>
