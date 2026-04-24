admin-categories = <b>{ -category-emoji } Categories</b>
    .order-btn = { -current } { sorting-order } { -current }
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Settings️
    .filters-btn = { -filter-emoji } Filters

admins-category-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admin-category = <b>{ -category-emoji } Category editing</b>

    <b>📜 Basic information:</b>
    { admin-category-name }
    { admin-category-description }
    { $updated_at ->
        [None] { -current } Created at: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Created at: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Last updated: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Items:</b>
    ├ Positions count: <code>{ $positions_amount }</code>
    { $is_archived ->
        [False] └ Items count: <code>{ $items_amount }</code>
        *[True] └ Items count: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Category is archived <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
    }
    .show-language-btn = Show in:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Name
    .description-btn = Description
    .media-btn = Media

admin-category-archive-confirmation = <b>🤔 Do you really want to archive category <code>{ $name }</code>?</b>

    <blockquote>⚠️ <b>ALL</b> category positions will also be archived</blockquote>

admin-category-delete-confirmation = <b>🤔 Do you really want to archive category { $name }</b>

    <blockquote>⚠️ Deleted category cannot be restored. <i><b>ALL</b> positions will also be deleted</i></blockquote>

admin-category-archive-all-confirmation = <b>🤔 Do you really want to archive <i>ALL</i> categories?</b>

    <blockquote>⚠️ Archived categories will become unavailable for purchase and editing.
    <b>ALL</b> category positions will also be archived</blockquote>

admin-category-delete-all-confirmation = <b>🤔 Do you really want to delete <i>ALL</i> categories?</b>

    <blockquote>⚠️ Deleted categories cannot be restored.
    <i>Only archived positions will be deleted.
    <b>ALL</b> positions will also be deleted</i></blockquote>
