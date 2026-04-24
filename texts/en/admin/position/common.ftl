admin-position-name =
    { -current } Name: <code>{ $name ->
        [None] { unknown.emoji } Not specified
        *[other] { $name }
    }</code>

position-price-row = { $is_last ->
    [True] └ <code>{ $amount }{ currency.symbol }</code>
    *[False] ├ <code>{ $amount }{ currency.symbol }</code>
}

admin-position-description =
    { -current } Description: { $has_description ->
        [True] { $description ->
            [None] { unknown.emoji } Not specified
            *[other] { $description }
            }
        *[False] { unknown.emoji } Absent
    }
