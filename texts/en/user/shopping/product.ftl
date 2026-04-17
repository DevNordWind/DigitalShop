user-shopping-category = { $has_categories ->
    [True] <b>{ -category-emoji } Categories</b>
    *[False] <b>🛒 Shopping temporarily unavailable</b>
}
    .btn = { $name }

default-position-btn = { $name } | { $amount }{ currency.symbol } | { $items_amount } pcs

user-shopping-position = <b>{ -position-emoji } Positions</b>

    { $category_description ->
        [None] { -current } Category: { $category_name }
        *[other] { -current } Category: { $category_name }
             { -current } Description: { $category_description }
    }
    .btn = { $items_amount ->
        [0] { default-position-btn }
        *[other] { $type ->
            [STOCK] { default-position-btn }
            [FIXED] { $name } | { $amount }{ currency.symbol } | ♾️
            *[other] { default-position-btn }
        }
    }

default-user-position =
    { -current } Quantity: { $items_amount ->
        [0] <code>{ $items_amount } pcs</code>
        *[other] { $type ->
            [STOCK] <code>{ $items_amount } pcs</code>
            [FIXED] ♾️
            *[other] <code>{ $items_amount } pcs</code>
        }
    }
    { -current } Price: <code>{ $amount }{ currency.symbol }</code>

user-position = <b>{ -position-emoji } { $name }</b>

    { $description ->
        [None] { default-user-position }
        *[other] { default-user-position }
            { -current } Description: { $description }
    }
    .buy-btn = Buy


user-position-items-amount-stock = <b>✏️ Enter quantity</b>

    { -current } Available: <code>{ $count } pcs</code>