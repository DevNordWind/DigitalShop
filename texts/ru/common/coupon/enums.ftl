coupon-status = { $status ->
    [ACTIVE] Активные
    [EXPIRED] Истёкшие
    [REVOKED] Отозванные
    [NOT_STARTED] Ожидающие
    *[other] { unknown }
    }

coupon-type = { $type ->
    [FIXED] Фиксированная сумма
    [COEFFICIENT] Процент от суммы заказа
    *[other] { unknown }
}

