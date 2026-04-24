warehouse-type = { $type ->
    [STOCK] Пополняемое
    [FIXED] Фиксированное
    *[other] { unknown }
}

item-status-plural = { $item_status ->
    [AVAILABLE] Продающиеся
    [SOLD] Проданные
    [RESERVED] Зарезервированные
    [ARCHIVED] Заархивированные
    *[other] { unknown }
}

position-status-plural = { $status ->
    [AVAILABLE] Доступные
    [ARCHIVED] Заархивированные
    *[other] { unknown }
}
