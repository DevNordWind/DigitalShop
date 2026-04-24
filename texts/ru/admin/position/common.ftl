admin-position-name =
    { -current } Название: <code>{ $name ->
        [None] { unknown.emoji } Не указано
        *[other] { $name }
    }</code>

position-price-row = { $is_last ->
    [True] └ <code>{ $amount }{ currency.symbol }</code>
    *[False] ├ <code>{ $amount }{ currency.symbol }</code>
}

admin-position-description =
    { -current } Описание: { $has_description ->
        [True] { $description ->
            [None] { unknown.emoji } Не указано
            *[other] { $description }
            }
        *[False] { unknown.emoji } Отсутствует
    }
