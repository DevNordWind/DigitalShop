admin-category-edit-name = <b>✏️ Введи новое название категории</b>

    { -current } Текущее название: <code>{ $name ->
        [None] Не указано на данном языке
        *[other] { $name }
    }</code>
    .default-lang-btn = { -langs-emoji } Язык по умолчанию
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-category-edit-name-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>⚠️ Перед сменой языка по умолчанию, убедись, что он заполнен</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-category-edit-description = <b>✏️ Введи новое описание категории</b>

    { -current } Текущее описание: { $has_description ->
        [True] { $description ->
            [None] Не указано на данном языке
            *[other] { $description }
            }
        *[False] { unknown.emoji } Отсутствует.

            <blockquote> ⚠️ Выбранный язык станет языком по умолчанию</blockquote>
    }

    .default-lang-btn = { -langs-emoji } Язык по умолчанию
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-category-edit-description-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>⚠️ Перед сменой языка по умолчанию, убедись, что он заполнен</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }


admin-category-edit-media = <b>{ -media-emoji } Редактирование медиа</b>

    <blockquote>ℹ️ Отправь фото, видео или GIF</blockquote>
