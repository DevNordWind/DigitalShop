order-payment-method = { $method ->
    [None] С баланса
    *[other] { payment-method }
}

user-shopping-order-line = { $is_last ->
    [False] ├ <b>{ $position_name }:</b> { $items_amount }шт. <code>{ $total_price }{ currency.symbol }</code>
    *[True] └ <b>{ $position_name }:</b> { $items_amount }шт. <code>{ $total_price }{ currency.symbol }</code>
}

user-shopping-order = <b>{ -order-emoji } Сформирован заказ <code>#{ $order_id }</code></b>

    { $items_amount ->
        [1] { user-shopping-position-default }
        *[other] { user-shopping-position-default  }
            └ Кол-во товаров: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -coupon-emoji } Купон:</b> { $is_applied_coupon ->
        [False] ❌ не указан
        *[True] <code>{ $code }</code> - <i>{ $coupon_discount }</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    💸 Итого: <code>{ $total_amount }{ currency.symbol }</code>

    <blockquote>🔥 Перейти к оплате?</blockquote>
    .order-cancelled-call = ❌ Заказ отменён
    .to-payment-btn = { -payment-method-emoji } К оплате
    .coupon-btn = { -coupon-emoji } Использовать купон
    .cancel-btn = ❌ Отменить

user-shopping-order-select-payment = { -payment-method-emoji } Способ оплаты
    .wallet-btn = С кошелька
    .payment-btn = { payment-method }

user-shopping-order-payment = <b>{ -order-emoji } Заказ <code>#{ $order_id }</code></b>

    🧾 Платёж <code>{ $payment_id }</code>
    { -current } Сумма оплаты: <code>{ $to_pay_amount }{ currency.symbol }</code>
    { -current } У вас имеется 15 минут на оплату

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Оплатить
    .check-btn = 🔄 Проверить оплату
    .check = { $status ->
        [PAID] ✅ Оплата обнаружена
        *[other] ⏳ Ожидаем оплату
    }
    .cancel-btn = ❌ Отменить
    .cancel = ❌ Заказ отменён
    .no-items-available-call = { -item-emoji } Товаров нет в наличии. ❌ Заказ отменён

user-shopping-order-coupon-code = <b>✏️ Введите код активации купона</b>

user-shopping-order-payment-confirmed = <b>✅ Заказ подтверждён</b>

    <b>{ -current } ID заказа:</b> <code>{ $order_id }</code>
    <b>{ -current } Сумма заказа:</b> <code>{ $amount } { currency.symbol }</code>

    <blockquote>♥️ Спасибо за покупку</blockquote>
    .to-order-btn = 🛒 К заказу
