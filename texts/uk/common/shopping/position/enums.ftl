warehouse-type = { $type ->
    [UNLIMITED] Поповнюваний
    [FIXED] Фіксований
    *[other] { unknown }
}

item-status-plural = { $item_status ->
    [AVAILABLE] Доступні для продажу
    [SOLD] Продані
    [RESERVED] Зарезервовані
    [ARCHIVED] Заархівовані
    *[other] { unknown }
}

position-status-plural = { $status ->
    [AVAILABLE] Доступні
    [ARCHIVED] Заархівовані
    *[other] { unknown }
}
