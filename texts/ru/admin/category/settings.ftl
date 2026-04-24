admin-category-settings = <b>⚙️ Настройки️</b>

    .default-lang-btn = { -langs-emoji } Язык по умолчанию
    .show-with-no-items-btn = { -item-emoji } Категории без товаров
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-category-default-lang = <b>{ -langs-emoji } Язык по умолчанию</b>

    <blockquote>ℹ️ <b>Язык по умолчанию</b> становится <b>обязательным</b> при создании новых категорий. <b>Авто-перевод</b> на другие языки осуществляется на его основе</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
