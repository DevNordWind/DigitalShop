user-orders = <b>{ -order-emoji } Заказы</b>
    .filters-btn = { -filter-emoji } Фильтры
    .btn = { $count ->
        [1] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        [0] { $position_name } | { -date-emoji } { DATETIME($created_at, dateStyle: "short") }
        *[other] { $position_name }| { $count }шт. | { -date-emoji} { DATETIME($created_at, dateStyle: "short") }
    }

user-orders-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { order-status.plural } { -current }
        *[other] { order-status.plural }
    }

user-order-default-position = <b>{ -position-emoji } Позиция:</b> <code>{ $position_name }</code>

user-order-coupon = <code>{ $code }</code> - скидка составила <code>{ $amount }{ currency.symbol }</code>

user-order = <b>{ -order-emoji } Заказ <code>{ $order_id }</code></b>

    { $items_amount ->
        [0] { user-order-default-position }
        [1] { user-order-default-position }
        *[other] { user-order-default-position }
            └ Кол-во товаров: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -current } Сумма:</b> <code>{ $total_amount }{ currency.symbol }</code>
    ├ Купон: { $is_applied_coupon ->
        [False] не был применён
        *[True] { $coupon_row }
    }
    └ Способ оплаты: { $has_source ->
        [False] не был выбран
        *[True] { order-source }
    }

    <blockquote>{ $status ->
        [CREATED] ℹ️ Заказ ожидает оплату
        [PENDING] ℹ️ Заказ ожидает оплату
        [CONFIRMED] { order-status.emoji } Заказ подтверждён { $confirmed_at }
        [CANCELLED] { order-status.emoji } Заказ отменён { $cancelled_at }
        [FAILED] { status.emoji } Заказ отменён { $failed_at }
        *[other] { unknown }
    }</blockquote>
    .upload-items = 💾 Выгрузить
