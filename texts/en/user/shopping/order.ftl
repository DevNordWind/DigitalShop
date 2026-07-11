order-payment-method = { $method ->
    [None] From balance
    *[other] { payment-method }
}

user-shopping-position-default = <b>{ -position-emoji } Position:</b> <code>{ $position_name }</code>


user-shopping-order = <b>{ -order-emoji } Order <code>#{ $order_id }</code> has been created</b>
    { $items_amount ->
        [1] { user-shopping-position-default }
        *[other] { user-shopping-position-default  }
            └ Items count: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -coupon-emoji } Coupon:</b> { $is_applied_coupon ->
        [False] ❌ not specified
        *[True] <code>{ $code }</code> - <i>{ $coupon_discount }</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    💸 Total: <code>{ $total_amount }{ currency.symbol }</code>
    <blockquote>🔥 Proceed to payment?</blockquote>
    .order-cancelled-call = ❌ Order cancelled
    .to-payment-btn = { -payment-method-emoji } Pay
    .coupon-btn = { -coupon-emoji } Use coupon
    .cancel-btn = ❌ Cancel

user-shopping-order-select-payment = { -payment-method-emoji } Payment Method
    .wallet-btn = From Wallet
    .payment-btn = { payment-method }

user-shopping-order-payment = <b>{ -order-emoji } Order <code>#{ $order_id }</code></b>

    🧾 Payment <code>{ $payment_id }</code>
    { -current } Payment amount: <code>{ $to_pay_amount }{ currency.symbol }</code>
    { -current } You have 15 minutes to complete the payment

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Pay
    .check-btn = 🔄 Check Payment
    .check = { $status ->
        [PAID] ✅ Payment detected
        *[other] ⏳ Waiting for payment
    }
    .cancel-btn = ❌ Cancel
    .cancel = ❌ Order cancelled
    .no-items-available-call = { -item-emoji } Items out of stock. ❌ Order cancelled

user-shopping-order-coupon-code = <b>✏️ Enter coupon activation code</b>

user-shopping-order-payment-confirmed = <b>✅ Order confirmed</b>

    <b>{ -current } Order ID:</b> <code>{ $order_id }</code>
    <b>{ -current } Order total:</b> <code>{ $amount } { currency.symbol }</code>

    <blockquote>♥️ Thank you for your purchase</blockquote>
    .to-order-btn = 🛒 Go to Order
