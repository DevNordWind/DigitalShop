admin-position-edit-name = <b>✏️ Введи новое название позиции</b>

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

admin-position-edit-name-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>⚠️ Перед сменой языка по умолчанию, убедись, что он заполнен</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>⚠️ Перед сменой языка по умолчанию, убедись, что он заполнен</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description = <b>✏️ Введи новое описание позиции</b>

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

admin-position-edit-base-currency = <b>🪙 Валюта по умолчанию</b>

    <blockquote>ℹ️ <b>Валюта по умолчанию</b> становится базовой валютой при конвертации</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }

admin-position-edit-price = <b>✏️ Введи цену позиции</b>

    <b>{ -current } Текущие цены:</b>
    { $prices }
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .base-currency-btn = 🪙 Валюта по умолчанию
    .convert-btn = Конвертировать в остальные валюты

editing-mode = { $mode ->
    [REPLACE] 🔁 Замена
    [ADD] ➕ Добавление
    *[other] { unknown }
}

admin-position-edit-media = <b>{ -media-emoji } Редактирование медиа</b>

    <blockquote>ℹ️ Отправь фото, видео или GIF</blockquote>
    .mode-btn = Режим редактирования
    .btn = { $is_current ->
        [True] { -current } { editing-mode } { -current }
        *[False] { editing-mode }
    }
