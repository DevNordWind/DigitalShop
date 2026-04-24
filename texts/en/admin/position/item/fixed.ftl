admin-position-fixed-item =
    { $item_value }

    { -time-emoji } Added: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>


admin-position-warehouse-fixed = <b>{ -item-emoji } Items</b>

    { -current } Warehouse type: { warehouse-type }
    { -current } Item: { $has_item ->
        [False] { unknown.emoji } not added
        *[True] { $is_archived ->
            [False] { admin-position-fixed-item }
            *[True] { admin-position-fixed-item }

        <blockquote>🗄 Item archived <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        }
    }
    .replace-btn = 🔁 Replace
    .warehouse-btn = 📦 Warehouse
    .archive-btn = 🗄 Archive

admin-position-warehouse-archive-confirmation-fixed = <b>🤔 Are you sure you want to archive the item?</b>

    <blockquote>⚠️ Archived item will become unavailable for purchase and editing</blockquote>

admin-position-warehouse-delete-confirmation-fixed = <b>🤔 Are you sure you want to delete the item?</b>

    <blockquote>⚠️ Deleted item will be <b>IMPOSSIBLE</b> to restore</blockquote>

admin-position-warehouse-archive-fixed = <b>🗄 Archive</b>
    .btn = { $item_value } | { -date-emoji }{ DATETIME($archived_at, dateStyle: "short", timeStyle: "short")}

admin-position-warehouse-archived-item-fixed = <b>{ -item-emoji } Item</b>

    <b>{ -current } Content:</b> <code>{ $item_value }</code>

    { -time-emoji } Added: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    └ Archived: <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i>

admin-position-warehouse-replace-fixed = <b>🔁 Replace item</b>

    <blockquote>ℹ️ Send item content as text.</blockquote>

admin-position-warehouse-add-fixed = <b>➕ Add item</b>

    <blockquote>ℹ️ Send item content as text.</blockquote>
