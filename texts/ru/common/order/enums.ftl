order-status = { $status ->
    [NEW] Новый
    [AWAITING_PAYMENT] Ожидает оплаты
    [CONFIRMED] Подтверждённый
    [CANCELLED] Отменён
    [FAILED] Завершён с ошибкой
    [EXPIRED] Истёк
    *[other] { unknown }
}
    .lower-case = { $status ->
        [NEW] новый
        [AWAITING_PAYMENT] ожидает оплаты
        [CONFIRMED] подтверждённый
        [CANCELLED] отменён
        [FAILED] завершён с ошибкой
        [EXPIRED] истёк
        *[other] { unknown }
    }
    .plural = { $status ->
        [NEW] Новые
        [AWAITING_PAYMENT] Ожидающие оплату
        [CONFIRMED] Подтверждённые
        [CANCELLED] Отменённые
        [FAILED] Завершённые с ошибкой
        [EXPIRED] Истёкшие
        *[other] { unknown }
    }
    .emoji = { $status ->
        [NEW] ⏳
        [AWAITING_PAYMENT] ⏳
        [CONFIRMED] ✅
        [CANCELLED] ❌
        [FAILED] ❌
        [EXPIRED] ❌
        *[other] { unknown }
    }



order-applied-coupon = { $type ->
    [PERCENT] Скидка { $percent }% от суммы заказа
    [FIXED] Скидка { $amount }{ currency.symbol } от суммы заказа
    *[other] { unknown }
}

order-source = { $source_type ->
    [WALLET] Баланс кошелька
    [PAYMENT] { payment-method }
    *[other] { unknown }
}
