coupon-discount = { $type ->
    [FIXED] Знижка { $amount }{ currency.symbol } від суми замовлення
    [COEFFICIENT] Знижка { $percent }% від суми замовлення
    *[other] { unknown }
}
