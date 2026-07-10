user-orders = <b>{ -order-emoji } Orders</b>
    .filters-btn = { -filter-emoji } Filters
    .btn = { $count ->
        [1] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        [0] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        *[other] { $position_name } | { $count} pcs. | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
    }

user-orders-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { order-status.plural } { -current }
        *[other] { order-status.plural }
    }

user-order-default-position = <b>{ -position-emoji } Item:</b> <code>{ $position_name }</code>

user-order-coupon = <code>{ $code }</code> — you saved <code>{ $amount }{ currency.symbol }</code>

user-order = <b>{ -order-emoji } Order <code>{ $order_id }</code></b>

    { $items_amount ->
        [0] { user-order-default-position }
        [1] { user-order-default-position }
        *[other] { user-order-default-position }
            └ Number of items: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -current } Total:</b> <code>{ $total_amount }{ currency.symbol }</code>
    ├ Coupon: { $is_applied_coupon ->
        [False] not applied
        *[True] { $coupon_row }
    }
    └ Payment method: { $has_source ->
        [False] not selected
        *[True] { order-source }
    }

    <blockquote>{ $status ->
        [NEW] ℹ️ Order is awaiting payment
        [AWAITING_PAYMENT] ℹ️ Order is awaiting payment
        [CONFIRMED] { order-status.emoji } Order confirmed { $confirmed_at }
        [CANCELLED] { order-status.emoji } Order cancelled { $cancelled_at }
        [FAILED] { status.emoji } Order cancelled { $failed_at }
        [EXPIRED] { status.emoji } Order expired
        *[other] { unknown }
    }</blockquote>
    .upload-items = 💾 Export
