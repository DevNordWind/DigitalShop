admin-position-edit-name = <b>✏️ Enter new position name</b>

    { -current } Current name: <code>{ $name ->
        [None] Not specified
        *[other] { $name }
    }</code>
    .default-lang-btn = { -langs-emoji } Default language
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-position-edit-name-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>⚠️ Before changing the default language, make sure it is filled</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>⚠️ Before changing the default language, make sure it is filled</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-edit-description = <b>✏️ Enter new position description</b>

    { -current } Current description: { $has_description ->
        [True] { $description ->
            [None] Not specified
            *[other] { $description }
            }
        *[False] { unknown.emoji } Missing

            <blockquote>⚠️ Selected language will become default language</blockquote>
    }

    .default-lang-btn = { -langs-emoji } Default language
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-position-edit-base-currency = <b>🪙 Default currency</b>

    <blockquote>ℹ️ <b>Default currency</b> becomes the base currency for conversion</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }

admin-position-edit-price = <b>✏️ Enter position price</b>

    <b>{ -current } Current prices:</b>
    { $prices }
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .base-currency-btn = 🪙 Default currency
    .convert-btn = Convert to other currencies

editing-mode = { $mode ->
    [REPLACE] 🔁 Replace
    [ADD] ➕ Add
    *[other] { unknown }
}

admin-position-edit-media = <b>{ -media-emoji } Edit media</b>

    <blockquote>ℹ️ Send a photo, video or GIF</blockquote>
    .mode-btn = Edit mode
    .btn = { $is_current ->
        [True] { -current } { editing-mode } { -current }
        *[False] { editing-mode }
    }
