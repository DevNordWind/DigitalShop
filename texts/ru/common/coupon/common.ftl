coupon-discount = { $type ->
    [FIXED] Скидка { $amount }{ currency.symbol } от суммы заказа
    [COEFFICIENT] Скидка { $percent }% от суммы заказа
    *[other] { unknown }
}
