order-payment-method = { $method ->
    [None] З балансу
    *[other] { payment-method }
}

user-shopping-order-line = { $is_last ->
    [False] ├ <b>{ $position_name }:</b> { $items_amount }шт. <code>{ $total_price }{ currency.symbol }</code>
    *[True] └ <b>{ $position_name }:</b> { $items_amount }шт. <code>{ $total_price }{ currency.symbol }</code>
}

user-shopping-order = <b>{ -order-emoji } Сформовано замовлення <code>#{ $order_id }</code></b>
    { $items_amount ->
        [1] { user-shopping-position-default }
        *[other] { user-shopping-position-default  }
            └ Кількість товарів: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -coupon-emoji } Купон:</b> { $is_applied_coupon ->
        [False] ❌ не вказано
        *[True] <code>{ $code }</code> - <i>{ $coupon_discount }</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    💸 Разом: <code>{ $total_amount }{ currency.symbol }</code>
    <blockquote>🔥 Перейти до оплати?</blockquote>
    .order-cancelled-call = ❌ Замовлення скасовано
    .to-payment-btn = { -payment-method-emoji } До оплати
    .coupon-btn = { -coupon-emoji } Використати купон
    .cancel-btn = ❌ Скасувати

user-shopping-order-select-payment = { -payment-method-emoji } Спосіб оплати
    .wallet-btn = З гаманця
    .payment-btn = { payment-method }

user-shopping-order-payment = <b>{ -order-emoji } Замовлення <code>#{ $order_id }</code></b>

    🧾 Платіж <code>{ $payment_id }</code>
    { -current } Сума оплати: <code>{ $to_pay_amount }{ currency.symbol }</code>
    { -current } У вас є 15 хвилин на оплату

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Оплатити
    .check-btn = 🔄 Перевірити оплату
    .check = { $status ->
        [PAID] ✅ Оплату виявлено
        *[other] ⏳ Очікуємо оплату
    }
    .cancel-btn = ❌ Скасувати
    .cancel = ❌ Замовлення скасовано
    .no-items-available-call = { -item-emoji } Товарів немає в наявності. ❌ Замовлення скасовано

user-shopping-order-coupon-code = <b>✏️ Введіть код активації купона</b>

user-shopping-order-payment-confirmed = <b>✅ Замовлення підтверджено</b>

    <b>{ -current } ID замовлення:</b> <code>{ $order_id }</code>
    <b>{ -current } Сума замовлення:</b> <code>{ $amount } { currency.symbol }</code>

    <blockquote>♥️ Дякуємо за покупку</blockquote>
    .to-order-btn = 🛒 До замовлення
