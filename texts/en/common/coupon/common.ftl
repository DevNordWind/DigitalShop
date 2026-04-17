coupon-discount = { $type ->
    [FIXED] Discount { $amount }{ currency.symbol } from order total
    [COEFFICIENT] Discount { $percent }% from order total
    *[other] { unknown }
}