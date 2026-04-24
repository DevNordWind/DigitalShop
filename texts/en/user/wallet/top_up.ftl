top-up-input-amount = <b>✏️ Enter the top-up amount in <code>{ $currency }</code></b>
    .another-wallet-btn = { -wallet-emoji } Choose another wallet

top-up-select-currency = <b>{ -wallet-emoji } Select currency</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[other] { $currency }
    }

top-up-select-payment-method = <b>{ -payment-method-emoji } Select payment method</b>
    .btn = { payment-method }

payment-warning = { $method ->
    [CRYPTO_PAY] ℹ️ If the payment was not credited automatically, click <code>Check payment</code>
    *[other] Unknown payment method
}

top-up-payment = <b>📥 Top up balance</b>

    🧾 Payment <code>{ $payment_id }</code>
    { -current } To pay: <code>{ $amount }{ currency.symbol }</code>
    { -current } You have 3 hours to pay the invoice

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Proceed to payment
    .check-btn = 🔄 Check payment
    .check = { $status ->
        [PAID] ✅ Payment detected
        *[other] ⏳ Waiting for payment
    }
    .cancel-btn = ❌ Cancel
    .cancel = ❌ Order cancelled
