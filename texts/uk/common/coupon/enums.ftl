coupon-status = { $status ->
    [ACTIVE] Активні
    [EXPIRED] Із завершеним терміном дії
    [REVOKED] Відкликані
    [NOT_STARTED] Очікують активації
    *[other] { unknown }
    }

coupon-type = { $type ->
    [FIXED] Фіксована сума
    [COEFFICIENT] Відсоток від суми замовлення
    *[other] { unknown }
}
