payment-method = { $method ->
    [CRYPTO_PAY] Crypto Bot
    *[other] { unknown }
}

commission-type = { $type ->
    [SHOP] С магазина
    [CUSTOMER] С покупателя
    *[other] { unknown }
}