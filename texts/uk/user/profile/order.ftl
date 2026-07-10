user-orders = <b>{ -order-emoji } Замовлення</b>
    .filters-btn = { -filter-emoji } Фільтри
    .btn =
        Замовлення від { -date-emoji } { DATETIME($created_at, dateStyle: "short") }

user-orders-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { order-status.plural } { -current }
        *[other] { order-status.plural }
    }

user-order-default-position = <b>{ -position-emoji } Позиція:</b> <code>{ $position_name }</code>

user-order-coupon = <code>{ $code }</code> - знижка склала <code>{ $amount }{ currency.symbol }</code>

user-order = <b>{ -order-emoji } Замовлення <code>{ $order_id }</code></b>

    <b>{ -position-emoji } Всього позицій: <code>{ $positions_amount }шт.</code></b>
    { $lines }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -current } Сума:</b> <code>{ $total_amount }{ currency.symbol }</code>
    ├ Купон: { $is_applied_coupon ->
        [False] не було застосовано
        *[True] { $coupon_row }
    }
    └ Спосіб оплати: { $has_source ->
        [False] не було обрано
        *[True] { order-source }
    }

    <blockquote>{ $status ->
        [CREATED] ℹ️ Замовлення очікує оплату
        [PENDING] ℹ️ Замовлення очікує оплату
        [CONFIRMED] { order-status.emoji } Замовлення підтверджено { $confirmed_at }
        [CANCELLED] { order-status.emoji } Замовлення скасовано { $cancelled_at }
        [FAILED] { status.emoji } Замовлення скасовано { $failed_at }
        *[other] { unknown }
    }</blockquote>
    .upload-items = 💾 Завантажити
