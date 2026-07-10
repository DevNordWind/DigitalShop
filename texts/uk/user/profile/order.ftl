user-orders = <b>{ -order-emoji } Замовлення</b>
    .filters-btn = { -filter-emoji } Фільтри
    .btn = { $count ->
        [1] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        [0] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        *[other] { $position_name } | { $count} шт. | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
    }

user-orders-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { order-status.plural } { -current }
        *[other] { order-status.plural }
    }

user-order-default-position = <b>{ -position-emoji } Позиція:</b> <code>{ $position_name }</code>

user-order-coupon = <code>{ $code }</code> — знижка склала <code>{ $amount }{ currency.symbol }</code>

user-order = <b>{ -order-emoji } Замовлення <code>{ $order_id }</code></b>

    { $items_amount ->
        [0] { user-order-default-position }
        [1] { user-order-default-position }
        *[other] { user-order-default-position }
            └ Кількість товарів: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -current } Сума:</b> <code>{ $total_amount }{ currency.symbol }</code>
    ├ Купон: { $is_applied_coupon ->
        [False] не застосовано
        *[True] { $coupon_row }
    }
    └ Спосіб оплати: { $has_source ->
        [False] не вибрано
        *[True] { order-source }
    }

    <blockquote>{ $status ->
        [NEW] ℹ️ Замовлення очікує оплату
        [AWAITING_PAYMENT] ℹ️ Замовлення очікує оплату
        [CONFIRMED] { order-status.emoji } Замовлення підтверджено { $confirmed_at }
        [CANCELLED] { order-status.emoji } Замовлення скасовано { $cancelled_at }
        [FAILED] { status.emoji } Замовлення скасовано { $failed_at }
        [EXPIRED] { status.emoji } Термін дії замовлення минув
        *[other] { unknown }
    }</blockquote>
    .upload-items = 💾 Експортувати
