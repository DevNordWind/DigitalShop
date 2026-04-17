coupon-valid-until = { $valid_until ->
    [None] Perpetual
    *[other] { DATETIME($valid_until, dateStyle: "medium", timeStyle: "medium")}
}

coupon-amount-row = { $is_last ->
    [True] └ <code>{ $amount }{ currency.symbol }</code>
    *[False] ├ <code>{ $amount }{ currency.symbol }</code>
}