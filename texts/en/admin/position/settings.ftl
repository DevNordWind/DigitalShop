admin-position-settings = <b>⚙️ Settings</b>

    .default-lang-btn = { -langs-emoji } Default language
    .default-currency-btn = 🪙 Default currency
    .show-with-no-items-btn = { -item-emoji } Positions without items
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-position-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>ℹ️ <b>Default language</b> becomes <b>required</b> when creating new positions. <b>Auto-translation</b> to other languages is based on it</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-default-currency = <b>🪙 Default currency</b>

    <blockquote>ℹ️ <b>Default currency</b> becomes the base currency for conversions</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }