admin-positions-categories = <b>{ -category-emoji } Select category</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Settings
    .filters-btn = { -filter-emoji } Filters

admin-positions-category-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admins-position-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { position-status-plural } { -current }
        *[other] { position-status-plural }
    }

admin-positions = <b>{ -position-emoji } Positions</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Settings
    .filters-btn = { -filter-emoji } Filters

admin-position = <b>{ -position-emoji } Edit position</b>

    <b>📜 General information:</b>
    { admin-position-name }
    { admin-position-description }
    { $updated_at ->
        [None] { -current } Creation date: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Creation date: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Last update: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Prices:</b>
    { $prices }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Items:</b>
    { $is_archived ->
        [False] └ Items count: <code>{ $items_amount }</code>
        *[True] └ Items count: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Position is archived</blockquote>
    }
    .show-language-btn = Show in:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Name
    .description-btn = Description
    .media-btn = Media
    .price-btn = Prices
    .items-btn = Items

admin-position-archive-confirmation = <b>🤔 Do you really want to archive position <code>{ $name }</code>?</b>

    <blockquote>⚠️ Archived position will become unavailable for purchase and editing</blockquote>

admin-position-delete-confirmation = <b>🤔 Do you really want to delete position <code>{ $name }</code>?</b>

    <blockquote>⚠️ Deleted position CANNOT be restored</blockquote>

admin-position-archive-all-confirmation = <b>🤔 Do you really want to archive ALL positions?</b>

    <blockquote>⚠️ Archived positions will become unavailable for purchase and editing</blockquote>

admin-position-delete-all-confirmation = <b>🤔 Do you really want to delete ALL positions?</b>

    <blockquote>⚠️ Deleted positions CANNOT be restored. <i>Only archived positions will be deleted</i></blockquote>
