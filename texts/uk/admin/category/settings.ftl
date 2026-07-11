admin-category-settings = <b>⚙️ Налаштування</b>

    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .show-with-no-items-btn = { -item-emoji } Категорії без товарів
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-category-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>ℹ️ <b>Мова за замовчуванням</b> стає <b>обов'язковою</b> при створенні нових категорій. <b>Автопереклад</b> на інші мови здійснюється на її основі</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
