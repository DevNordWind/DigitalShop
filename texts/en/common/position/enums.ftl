warehouse-type = { $type ->
    [STOCK] Refillable
    [FIXED] Fixed
    *[other] { unknown }
}

item-status-plural = { $item_status ->
    [AVAILABLE] For sale
    [SOLD] Sold
    [RESERVED] Reserved
    [ARCHIVED] Archived
    *[other] { unknown }
}

position-status-plural = { $status ->
    [AVAILABLE] Available
    [ARCHIVED] Archived
    *[other] { unknown }
}
