top-up-input-amount = <b>✏️ Введи суму поповнення в <code>{ $currency }</code></b>
    .another-wallet-btn = { -wallet-emoji } Вибрати інший гаманець

top-up-select-currency = <b>{ -wallet-emoji } Вибери валюту</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[other] { $currency }
    }

top-up-select-payment-method = <b>{ -payment-method-emoji } Вибери спосіб оплати</b>
    .btn = { payment-method }

payment-warning = { $method ->
    [CRYPTO_PAY] ℹ️ Якщо оплата не зарахувалася автоматично, натисни на <code>Перевірити оплату</code>
    [LOLZ_TEAM] ℹ️ Якщо оплата не зарахувалася автоматично, натисни на <code>Перевірити оплату</code>
    *[other] Невідомо
}

top-up-payment = <b>📥 Поповнення балансу</b>

    🧾 Платіж <code>{ $payment_id }</code>
    { -current } До сплати: <code>{ $amount }{ currency.symbol }</code>
    { -current } У вас є 3 години на оплату рахунку

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Перейти до оплати
    .check-btn = 🔄 Перевірити оплату
    .check = { $status ->
        [PAID] ✅ Оплату виявлено
        *[other] ⏳ Очікуємо оплату
    }
    .cancel-btn = ❌ Скасувати
    .cancel = ❌ Замовлення скасовано

top-up-payment-confirmed = <b>✅ Баланс успішно поповнено на <code>{ $amount }{ currency.symbol }</code></b>

    🧾 Платіж <code>{ $payment_id }</code>
