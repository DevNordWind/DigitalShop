payment-method = { $method ->
    [CRYPTO_PAY] Crypto Bot
    *[other] { unknown }
}

commission-type = { $type ->
    [SHOP] From shop
    [CUSTOMER] From customer
    *[other] { unknown }
}