top-up-input-amount = <b>✏️ Введи сумму пополнения в <code>{ $currency }</code></b>
    .another-wallet-btn = { -wallet-emoji } Выбрать другой кошелёк

top-up-select-currency = <b>{ -wallet-emoji } Выбери валюту</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[other] { $currency }
    }

top-up-select-payment-method = <b>{ -payment-method-emoji } Выбери способ оплаты</b>
    .btn = { payment-method }

payment-warning = { $method ->
    [CRYPTO_PAY] ℹ️ Если оплата не зачислилась автоматически, нажмите на <code>Проверить оплату</code>
    *[other] Неизвестно
}

top-up-payment = <b>📥 Пополнение баланса</b>

    🧾 Платёж <code>{ $payment_id }</code>
    { -current } К оплате: <code>{ $amount }{ currency.symbol }</code>
    { -current } У вас имеется 3 часа на оплату счета

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Перейти к оплате
    .check-btn = 🔄 Проверить оплату
    .check = { $status ->
        [PAID] ✅ Оплата обнаружена
        *[other] ⏳ Ожидаем оплату
    }
    .cancel-btn = ❌ Отменить
    .cancel = ❌ Заказ отменён
