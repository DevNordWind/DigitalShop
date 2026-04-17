admin-position-settings = <b>⚙️ Настройки️</b>

    .default-lang-btn = { -langs-emoji } Язык по умолчанию
    .default-currency-btn = 🪙 Валюта по умолчанию
    .show-with-no-items-btn = { -item-emoji } Позиции без товаров
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-position-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>ℹ️ <b>Язык по умолчанию</b> становится <b>обязательным</b> при создании новых позиций. <b>Авто-перевод</b> на другие языки осуществляется на его основе</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-default-currency = <b>🪙 Валюта по умолчанию</b>

    <blockquote>ℹ️ <b>Валюта по умолчанию</b> становится базовой валютой при конвертации</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
