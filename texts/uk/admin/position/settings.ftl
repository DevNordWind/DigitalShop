admin-position-settings = <b>⚙️ Налаштування️</b>

    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .default-currency-btn = 🪙 Валюта за замовчуванням
    .show-with-no-items-btn = { -item-emoji } Позиції без товарів
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-position-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>ℹ️ <b>Мова за замовчуванням</b> стає <b>обов'язковою</b> під час створення нових позицій. <b>Автопереклад</b> на інші мови здійснюється на її основі</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-position-default-currency = <b>🪙 Валюта за замовчуванням</b>

    <blockquote>ℹ️ <b>Валюта за замовчуванням</b> стає базовою валютою під час конвертації</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
