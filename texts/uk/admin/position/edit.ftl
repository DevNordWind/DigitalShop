admin-position-edit-name = <b>✏️ Введи нову назву позиції</b>

    { -current } Поточна назва: <code>{ $name ->
        [None] Не вказано цією мовою
        *[other] { $name }
    }</code>
    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти на інші мови

admin-position-edit-name-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>⚠️ Перед зміною мови за замовчуванням переконайся, що вона заповнена</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>⚠️ Перед зміною мови за замовчуванням переконайся, що вона заповнена</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description = <b>✏️ Введи новий опис позиції</b>

    { -current } Поточний опис: { $has_description ->
        [True] { $description ->
            [None] Не вказано цією мовою
            *[other] { $description }
            }
        *[False] { unknown.emoji } Відсутній.

            <blockquote> ⚠️ Обрана мова стане мовою за замовчуванням</blockquote>
    }

    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти на інші мови

admin-position-edit-base-currency = <b>🪙 Валюта за замовчуванням</b>

    <blockquote>ℹ️ <b>Валюта за замовчуванням</b> стає базовою валютою під час конвертації</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }

admin-position-edit-price = <b>✏️ Введи ціну позиції</b>

    <b>{ -current } Поточні ціни:</b>
    { $prices }
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .base-currency-btn = 🪙 Валюта за замовчуванням
    .convert-btn = Конвертувати в інші валюти

editing-mode = { $mode ->
    [REPLACE] 🔁 Заміна
    [ADD] ➕ Додавання
    *[other] { unknown }
}

admin-position-edit-media = <b>{ -media-emoji } Редагування медіа</b>

    <blockquote>ℹ️ Надішли фото, відео або GIF</blockquote>
    .mode-btn = Режим редагування
    .btn = { $is_current ->
        [True] { -current } { editing-mode } { -current }
        *[False] { editing-mode }
    }
