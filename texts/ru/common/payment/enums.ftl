payment-method = { $method ->
    [CRYPTO_PAY] Crypto Bot
    [LOLZ_TEAM] LolzTeam
    *[other] { unknown }
}

commission-type = { $type ->
    [SHOP] С магазина
    [CUSTOMER] С покупателя
    *[other] { unknown }
}
