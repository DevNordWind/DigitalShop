admin-category-create-view =  <b> { -category-emoji } Создание категории</b>

    <b>📜 Основная информация:</b>
    { admin-category-name }
    { admin-category-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Медиа:</b> { $has_media ->
        [False] Не добавлено
        *[True] Добавлено
    }

    <blockquote>🤔 Всё ли верно?</blockquote>
    .show-language-btn = Показать на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Название
    .description-btn = Описание
    .media-btn = Медиа

admin-category-create-name = <b>✏️ Введи название категории</b>

    { -current } Текущее название: <code>{ $name ->
        [None] { unknown.emoji } Не указано
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Заполнение имени на <i>{ lang.ins-lower-case }</i> является <b>обязательным</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-category-create-description = <b>✏️ Введи описание категории</b>

    { -current } Текущее описание: { $description ->
        [None] { unknown.emoji } Не указано
        *[other] { $description }
    }

    <blockquote>ℹ️ Заполнение описания на <i>{ lang.ins-lower-case }</i> является <b>обязательным</b>. <i>Поддерживается HTML форматирование</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-category-create-media = <b>{ -media-emoji } Добавление медиа</b>

    <blockquote>ℹ️ Отправь фото, видео или GIF</blockquote>
