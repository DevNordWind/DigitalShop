admin-category-name =
    { -current } Назва: <code>{ $name ->
        [None] { unknown.emoji } Не вказано
        *[other] { $name }
    }</code>

admin-category-description =
    { -current } Опис: { $has_description ->
        [True] { $description ->
            [None] { unknown.emoji } Не вказано
            *[other] { $description }
            }
        *[False] { unknown.emoji } Відсутній
    }
