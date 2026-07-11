admin-position-name =
    { -current } Назва: <code>{ $name ->
        [None] { unknown.emoji } Не вказано
        *[other] { $name }
    }</code>

position-price-row = { $is_last ->
    [True] └ <code>{ $amount }{ currency.symbol }</code>
    *[False] ├ <code>{ $amount }{ currency.symbol }</code>
}

admin-position-description =
    { -current } Опис: { $has_description ->
        [True] { $description ->
            [None] { unknown.emoji } Не вказано
            *[other] { $description }
            }
        *[False] { unknown.emoji } Відсутній
    }
