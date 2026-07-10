payment-method = { $method ->
    [CRYPTO_PAY] Crypto Bot
    [LOLZ_TEAM] LolzTeam
    *[other] { unknown }
}

commission-type = { $type ->
    [SHOP] З магазину
    [CUSTOMER] З покупця
    *[other] { unknown }
}
