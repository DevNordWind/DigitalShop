order-status = { $status ->
    [NEW] New
    [AWAITING_PAYMENT] Awaiting payment
    [CONFIRMED] Confirmed
    [CANCELLED] Cancelled
    [FAILED] Failed
    [EXPIRED] Expired
    *[other] { unknown }
}
    .lower-case = { $status ->
        [NEW] new
        [AWAITING_PAYMENT] awaiting payment
        [CONFIRMED] confirmed
        [CANCELLED] cancelled
        [FAILED] failed
        [EXPIRED] expired
        *[other] { unknown }
    }
    .plural = { $status ->
        [NEW] New
        [AWAITING_PAYMENT] Awaiting payment
        [CONFIRMED] Confirmed
        [CANCELLED] Cancelled
        [FAILED] Failed
        [EXPIRED] Expired
        *[other] { unknown }
    }
    .emoji = { $status ->
        [NEW] ⏳
        [AWAITING_PAYMENT] ⏳
        [CONFIRMED] ✅
        [CANCELLED] ❌
        [FAILED] ❌
        [EXPIRED] ⌛
        *[other] { unknown }
    }

order-applied-coupon = { $type ->
    [PERCENT] Discount { $percent }% from order total
    [FIXED] Discount { $amount }{ currency.symbol } from order total
    *[other] { unknown }
}

order-source = { $source_type ->
    [WALLET] Wallet balance
    [PAYMENT] { payment-method }
    *[other] { unknown }
}