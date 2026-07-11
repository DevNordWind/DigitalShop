user-shopping-category = { $has_categories ->
    [True] <b>{ -category-emoji } Категорії</b>
    *[False] <b>🛒 Покупки тимчасово недоступні</b>
}
    .btn = { $name }

default-position-btn = { $name } | { $amount }{ currency.symbol } | { $items_amount}шт

user-shopping-position = <b>{ -position-emoji } Позиції</b>

    { $category_description ->
        [None] { -current } Категорія: { $category_name }
        *[other] { -current } Категорія: { $category_name }
             { -current } Опис: { $category_description }
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
    { -current } К-сть товарів: { $items_amount ->
        [0] <code>{ $items_amount }шт.</code>
        *[other] { $type ->
            [STOCK] <code>{ $items_amount }шт.</code>
            [FIXED] ♾️
            *[other] <code>{ $items_amount }шт.</code>
        }
    }
    { -current } Вартість: <code>{ $amount }{ currency.symbol }</code>

user-position = <b>{ -position-emoji } { $name }</b>

    { $description ->
        [None] { default-user-position }
        *[other] { default-user-position }
            { -current } Опис: { $description }
    }
    .buy-btn = Купити

user-position-items-amount-stock = <b>✏️ Введіть кількість товарів</b>

    { -current } Доступно: <code>{ $count }шт.</code>
