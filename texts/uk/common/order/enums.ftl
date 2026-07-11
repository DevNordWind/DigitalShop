order-status = { $status ->
    [NEW] Нове
    [AWAITING_PAYMENT] Очікує оплати
    [CONFIRMED] Підтверджене
    [CANCELLED] Скасоване
    [FAILED] Завершене з помилкою
    [EXPIRED] Термін дії минув
    *[other] { unknown }
}
    .lower-case = { $status ->
        [NEW] нове
        [AWAITING_PAYMENT] очікує оплати
        [CONFIRMED] підтверджене
        [CANCELLED] скасоване
        [FAILED] завершене з помилкою
        [EXPIRED] термін дії минув
        *[other] { unknown }
    }
    .plural = { $status ->
        [NEW] Нові
        [AWAITING_PAYMENT] Ті, що очікують оплату
        [CONFIRMED] Підтверджені
        [CANCELLED] Скасовані
        [FAILED] Завершені з помилкою
        [EXPIRED] Із завершеним терміном дії
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
    [PERCENT] Знижка { $percent }% від суми замовлення
    [FIXED] Знижка { $amount }{ currency.symbol } від суми замовлення
    *[other] { unknown }
}

order-source = { $source_type ->
    [WALLET] Баланс гаманця
    [PAYMENT] { payment-method }
    *[other] { unknown }
}
