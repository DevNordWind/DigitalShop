admin-broadcast = <b>📢 Рассылка</b>

    <blockquote>ℹ️ Сообщение получат только те пользователи, чей язык есть в текстах рассылки</blockquote>
    .preview-btn = 🖼 Предпросмотр
    .buttons-btn = Кнопки
    .texts-btn = Текста
    .media-btn = { -media-emoji } Медиа
    .start-btn = ✅ Начать

admin-broadcast-preview-select-lang = <b>🖼 Предпросмотр</b>

    <blockquote>ℹ️ Выбери язык для предпросмотра</blockquote>
    .show-language-btn = Показать на:
    .lang-btn = { lang.emoji } { lang.ins }

admin-broadcast-preview =
    { $text ->
        [None] <blockquote>⚠️ Сообщения не будут разосланы на данном языке</blockquote>
        *[other] { $text }
    }

admin-broadcast-buttons = <b>Кнопки</b>

    <blockquote>ℹ️ Добавленные кнопки будут в сообщении рассылки</blockquote>
    .close-button-btn = Кнопка закрытия { $with_close_button ->
        [True] ✅
        *[False] ❌
    }
    .url-buttons-btn = URL-кнопки

admin-broadcast-buttons-url = <b>URL-кнопки</b>
    .btn = { $button_text }

admin-broadcast-buttons-url-create = <b>Создание URL-кнопки</b>

    <blockquote>⚠️ Убедись, что языки названий кнопки совпадают с языками текстов рассылки.
    <i>Созданная кнопка будет отображаться вверху под текстом текущего сообщения</i></blockquote>
    .show-language-btn = Показать на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .names-btn = Названия
    .url-btn = URL

admin-broadcast-buttons-url-text = <b>✏️ Введи название кнопки</b>

    { -current } Текущее название: { $name ->
        [None] { unknown.emoji } Не указано
        *[other] <code>{ $name }</code>
    }
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-buttons-url-url = <b>✏️ Введи URL кнопки</b>

    { -current } Текущий URL: { $url ->
        [None] { unknown.emoji } Не указан
        *[other] { $url }
    }
    .invalid = <b>❌ Неверный формат URL</b>

admin-broadcast-texts = <b>✏️ Введи текст рассылки</b>

    { -current } Текущий текст: { $text ->
        [None] { unknown.emoji } Не указано
        *[other] { $text }
    }

    <blockquote>ℹ️ Поддерживается HTML форматирование</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-media = <b>{ -media-emoji } Добавление медиа</b>

    <blockquote>ℹ️ Отправь фото, видео или GIF</blockquote>