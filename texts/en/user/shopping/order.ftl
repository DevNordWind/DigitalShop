user-shopping-position-default = <b>{ -position-emoji } Position:</b> <code>{ $position_name }</code>

order-payment-method = { $method ->
    [None] From balance
    *[other] { payment-method }
}

user-shopping-order = <b>{ -order-emoji } Order <code>#{ $order_id }</code> created</b>

    { $items_amount ->
        [1] { user-shopping-position-default }
        *[other] { user-shopping-position-default }
            └ Quantity: <code>{ $items_amount }</code>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -coupon-emoji } Coupon:</b> { $is_applied_coupon ->
        [False] ❌ not applied
        *[True] <code>{ $code }</code> - <i>{ $coupon_discount }</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    💸 Total: <code>{ $total_amount }{ currency.symbol }</code>

    <blockquote>🔥 Proceed to payment?</blockquote>
    .order-cancelled-call = ❌ Order cancelled
    .to-payment-btn = { -payment-method-emoji } Pay
    .coupon-btn = { -coupon-emoji } Apply coupon
    .cancel-btn = ❌ Cancel

user-shopping-order-select-payment = { -payment-method-emoji } Payment method
    .wallet-btn = From wallet
    .payment-btn = { payment-method }

user-shopping-order-payment = <b>{ -order-emoji } Order <code>#{ $order_id }</code></b>

    🧾 Payment <code>{ $payment_id }</code>
    { -current } Payment amount: <code>{ $to_pay_amount }{ currency.symbol }</code>
    { -current } You have 15 minutes to complete the payment

    <blockquote>{ payment-warning }</blockquote>
    .pay-btn = 💳 Pay
    .check-btn = 🔄 Check payment
    .check = { $status ->
        [PAID] ✅ Payment detected
        *[other] ⏳ Waiting for payment
    }
    .cancel-btn = ❌ Cancel
    .cancel = ❌ Order cancelled
    .no-items-available-call = { -item-emoji } Items not available. ❌ Order cancelled

user-shopping-order-coupon-code = <b>✏️ Enter coupon code</b>

user-shopping-order-new-items = <b>❌ Not enough items available</b>

    <b>{ -current } Available:</b> <code>{ $available } pcs</code>

    <blockquote>ℹ️ Enter a new quantity or cancel the order</blockquote>
    .cancel-btn = ❌ Cancel
    .cancel-msg = <b>{ -item-emoji } Items not available.</b>

            <blockquote>❌ Order cancelled</blockquote>
