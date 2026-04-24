admin-position-warehouse-stock = <b>{ -item-emoji } Items</b>

    { -current } Warehouse type: { warehouse-type }

    <blockquote>ℹ️ Click on an item to view its information</blockquote>
    .filters-btn = { -filter-emoji } Filters
    .btn = { $item_value } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }

admin-position-warehouse-stock-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order }{ -current }
    .status-btn = { $is_current ->
        [True] { -current } { item-status-plural } { -current }
        *[False] { item-status-plural }
    }

admin-position-warehouse-add-stock = <b>➕ Adding items</b>

    { -current } <b>Items</b> are separated by an empty line, for example:

    <code>Item data...</code>

    <code>Item data...</code>

    <code>Item data...</code>

    .success = <b>✅ Added <code>{ $count }</code> { items-plural-lower-case }</b>

admin-position-warehouse-item-stock = <b>{ -item-emoji } Item</b>

    <b>{ -current } Content:</b> <code>{ $item_value }</code>
    { -time-emoji } Added: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
    { $item_status ->
        [SOLD]
            ├ Reserved: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Sold: <i>{ DATETIME($sold_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [RESERVED] └ Reserved: <i>{ DATETIME($reserved_at, dateStyle: "medium", timeStyle: "medium")}</i>
        [ARCHIVED] {""}
        <blockquote>🗄 Item archived <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
        *[other] { unknown }
    }

admin-position-warehouse-archive-confirmation-stock = <b>🤔 Are you sure you want to archive the item?</b>

    <blockquote>⚠️ Archived item will become unavailable for purchase and editing</blockquote>

admin-position-warehouse-delete-confirmation-stock = <b>🤔 Are you sure you want to delete the item?</b>

    <blockquote>⚠️ Deleted item will be <b>IMPOSSIBLE</b> to restore</blockquote>

admin-position-warehouse-archive-all-confirmation-stock = <b>🤔 Are you sure you want to archive <b>ALL</b> items?</b>

    <blockquote>⚠️ Archived items will become unavailable for purchase and editing</blockquote>

admin-position-warehouse-delete-all-confirmation-stock = <b>🤔 Are you sure you want to delete <b>ALL</b> items?</b>

    <blockquote>⚠️ Deleted items will be <b>IMPOSSIBLE</b> to restore. <i>Only archived items will be deleted</i></blockquote>
