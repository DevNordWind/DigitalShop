admin-category-name =
    { -current } Название: <code>{ $name ->
        [None] { unknown.emoji } Не указано
        *[other] { $name }
    }</code>

admin-category-description =
    { -current } Описание: { $has_description ->
        [True] { $description ->
            [None] { unknown.emoji } Не указано
            *[other] { $description }
            }
        *[False] { unknown.emoji } Отсутствует
    }