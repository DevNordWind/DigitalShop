user-shopping-category = { $has_categories ->
    [True] <b>{ -category-emoji } Категории</b>
    *[False] <b>🛒 Покупки временно недоступны</b>
}
    .btn = { $name }

default-position-btn = { $name } | { $amount }{ currency.symbol } | { $items_amount}шт

user-shopping-position = <b>{ -position-emoji } Позиции</b>

    { $category_description ->
        [None] { -current } Категория: { $category_name }
        *[other] { -current } Категория: { $category_name }
             { -current } Описание: { $category_description }
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
    { -current } Кол-во товаров: { $items_amount ->
        [0] <code>{ $items_amount }шт.</code>
        *[other] { $type ->
            [STOCK] <code>{ $items_amount }шт.</code>
            [FIXED] ♾️
            *[other] <code>{ $items_amount }шт.</code>
        }
    }
    { -current } Стоимость: <code>{ $amount }{ currency.symbol }</code>

user-position = <b>{ -position-emoji } { $name }</b>

    { $description ->
        [None] { default-user-position }
        *[other] { default-user-position }
            { -current } Описание: { $description }
    }
    .buy-btn = Купить


user-position-items-amount-stock = <b>✏️ Введите количество товаров</b>

    { -current } Доступно: <code>{ $count }шт.</code>
